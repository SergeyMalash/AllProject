import os

from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView, RedirectView
from django.views.generic.detail import SingleObjectMixin
from shortener.forms import UrlForm, TagForm
from shortener.mixin import AddRequestForFormInitMixin
from shortener.models import Url, Tag
from shortener.services import get_obj_and_increase_counter, generate_slug


class IndexView(AddRequestForFormInitMixin, CreateView):
    model = Url
    template_name = 'shortener/index.html'
    form_class = UrlForm

    def form_valid(self, form):
        """Если URL создаёт авторизованный пользователь, то создаём URL в любом случае"""
        if self.request.user.is_anonymous is False:
            form.instance.user = self.request.user
            if not form.instance.slug:
                form.instance.slug = generate_slug()
            return super().form_valid(form)
        try:
            """
            Если создаёт аноним и уже есть URL от анонима, то перенаправляем на страницу ранее сохраненного URL -
            новый не создаём
            """
            self.object = Url.objects.get(full=form.instance.full, user=None)
            return HttpResponseRedirect(self.get_success_url())
        except Url.DoesNotExist:
            """Если URL не существует, то создаём новый"""
            form.instance.slug = generate_slug()
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_url', args=[self.object.slug])


class TagsListView(LoginRequiredMixin, ListView):
    template_name = 'shortener/tag_list.html'

    def get_queryset(self):
        return Tag.objects.filter(user=self.request.user)


class TagCreate(AddRequestForFormInitMixin, LoginRequiredMixin, CreateView):
    template_name = 'shortener/tag_create.html'
    model = Tag
    form_class = TagForm

    def get_success_url(self):
        return reverse('tags')

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.user = self.request.user
        instance.save()
        return HttpResponseRedirect(self.get_success_url())


class TagDetail(LoginRequiredMixin, ListView):
    template_name = 'shortener/tag_detail.html'

    def get_queryset(self):
        tag_obj = Tag.objects.get(title=self.kwargs['tag'], user=self.request.user)
        queryset = tag_obj.url_set.all()
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.kwargs['tag']
        return context


class TagUpdate(AddRequestForFormInitMixin, LoginRequiredMixin, UpdateView):
    template_name = 'shortener/tag_update.html'
    model = Tag
    form_class = TagForm

    def get_object(self, queryset=None):
        tag_obj = Tag.objects.get(title=self.kwargs['tag'], user=self.request.user)
        return tag_obj


class TagDelete(LoginRequiredMixin, DeleteView):
    template_name = 'shortener/tag_delete.html'
    model = Tag
    success_url = reverse_lazy('detail_account')

    # slug_field = 'title'
    # slug_url_kwarg = 'tag'

    def get_object(self, queryset=None):
        tag_obj = Tag.objects.get(title=self.kwargs['tag'], user=self.request.user)
        return tag_obj


class UrlsListView(LoginRequiredMixin, ListView):
    """Список ссылок, которые созданы пользователем"""
    template_name = 'shortener/urls_list.html'

    def get_queryset(self):
        return Url.objects.filter(user=self.request.user.pk)


class DetailUrl(DetailView):
    model = Url
    template_name = 'shortener/detail_url.html'

    def get_object(self, queryset=None):
        obj = Url.objects.get(slug=self.kwargs['slug'])
        if self.request.user == obj.user or obj.user is None:
            return obj
        raise PermissionDenied

    def get_context_data(self, **kwargs):
        context = super(DetailUrl, self).get_context_data(**kwargs)
        context['site_host'] = os.getenv('SITE_HOST')
        return context


class ChangeUrl(AddRequestForFormInitMixin, LoginRequiredMixin, UpdateView):
    model = Url
    template_name = 'shortener/change_url.html'
    form_class = UrlForm


class DeleteUrl(LoginRequiredMixin, DeleteView):
    model = Url
    template_name = 'shortener/delete_url.html'
    success_url = reverse_lazy('urls')


class RedirectUrl(RedirectView, SingleObjectMixin):
    model = Url

    def get_object(self, queryset=None):
        try:
            obj = Url.objects.get(slug=self.kwargs['slug'])
            return get_obj_and_increase_counter(obj)
        except Url.DoesNotExist:
            raise Http404

    def get_redirect_url(self, *args, **kwargs):
        return self.get_object().full
