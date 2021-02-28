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
from shortener.services import create_new_url, search_func, get_obj_and_increase_counter


class IndexView(AddRequestForFormInitMixin, CreateView):
    model = Url
    template_name = 'shortener/index.html'
    form_class = UrlForm
    object = None

    def form_valid(self, form):
        instance = form.save(commit=False)
        """Если URL создаёт авторизованный пользователь, то создаём его в любом случае"""
        if self.request.user.is_anonymous is False:
            instance.user = self.request.user
            self.object = create_new_url(instance)
            return super().form_valid(form)
        try:
            """
            Если создаёт аноним и уже есть URL от анонима, то перенаправляем на страницу ранее сохраненного URL -
            новый не создаём
            """
            self.object = Url.objects.get(full=instance.full, user=None)
            return HttpResponseRedirect(self.get_success_url())
        except Url.DoesNotExist:
            """Если URL не существует, то создаём новый"""
            self.object = create_new_url(instance)
            return super().form_valid(form)

    def get_success_url(self):
        return reverse('detail_url', args=[self.object.slug])


class SearchView(LoginRequiredMixin, ListView):
    template_name = 'shortener/search_result.html'
    search_text = None
    search_field = None
    paginate_by = 10

    def get(self, request, *args, **kwargs):
        self.search_text = self.request.GET.get('search_text', '')
        self.search_field = self.request.GET.get('search_field', 'slug')
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        search_result = search_func(self.search_text, self.search_field)
        return search_result

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=None, **kwargs)
        context['search_text'] = self.search_text
        context['search_field'] = self.search_field
        return context


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
        return super().form_valid(form)


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
    paginate_by = 10

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
