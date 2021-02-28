from django.views.generic import TemplateView


class FindChatView(TemplateView):
    template_name = 'anonymous/search_page_vue.html'
