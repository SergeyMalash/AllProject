from django.urls import path, re_path
from blog import views
urlpatterns = [
    re_path(r'^article/(?P<query>new|my|feed)/$', views.ListArticlesView.as_view(), name='list_article'),
    path('article/create/', views.ArticleCreateView.as_view(), name='create_article'),
    path('article/<slug>/', views.ArticleView.as_view(), name='article'),
    path('article/<slug>/delete/', views.ArticleDeleteView.as_view(), name='delete_article'),
    path('article/<slug>/update/', views.ArticleUpdateView.as_view(), name='update_article'),
]
