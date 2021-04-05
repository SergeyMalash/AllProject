from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, DeleteView, UpdateView

from blog.forms import ArticleForm
from blog.models import Article


class ArticleView(DetailView):
    model = Article
    template_name = 'blog/detail_article.html'


class ArticleCreateView(LoginRequiredMixin, CreateView):
    model = Article
    template_name = 'blog/create_article.html'
    form_class = ArticleForm

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(ArticleCreateView, self).form_valid(form)


class ListArticlesView(LoginRequiredMixin, ListView):
    template_name = 'blog/list_article.html'

    def get_queryset(self):
        if self.kwargs['query'] == 'my':
            return Article.objects.filter(user=self.request.user)
        if self.kwargs['query'] == 'feed':
            return Article.objects.filter(user=self.request.user)  # todo implement follower mechanic
        return Article.objects.all()


class ArticleDeleteView(LoginRequiredMixin, DeleteView):
    template_name = 'blog/delete_article.html'
    success_url = reverse_lazy('list_article', kwargs={'query': 'my'})

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)


class ArticleUpdateView(LoginRequiredMixin, UpdateView):
    template_name = 'blog/update_article.html'
    form_class = ArticleForm

    def get_queryset(self):
        return Article.objects.filter(user=self.request.user)
