from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from search.services import search_accounts, search_urls, search_articles


class SearchView(TemplateView, LoginRequiredMixin):
    template_name = 'search/search_result.html'
    search_text = None
    search_object = None

    def get(self, request, *args, **kwargs):
        self.search_text = self.request.GET.get('search_text', '')
        self.search_object = self.request.GET.get('search_object', None)
        return super().get(request, *args, **kwargs)

    def get_result(self):
        search_result = {
            'accounts': search_accounts(self),
            'urls': search_urls(self),
            'articles': search_articles(self)
        }
        return search_result

    def get_context_data(self, **kwargs):
        context = super(SearchView, self).get_context_data(**kwargs)
        context['search_text'] = self.search_text
        context['search_result'] = self.get_result()
        context['search_object'] = self.search_object
        return context
