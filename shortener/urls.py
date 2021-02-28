from django.urls import path

from shortener import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    # path('search/', views.SearchView.as_view(), name='search'),
    path('tags/', views.TagsListView.as_view(), name='tags'),
    path('tags/create/', views.TagCreate.as_view(), name='tag_create'),
    path('tags/<str:tag>/', views.TagDetail.as_view(), name='tag_detail'),
    path('tags/<str:tag>/update/', views.TagUpdate.as_view(), name='tag_update'),
    path('tags/<str:tag>/delete/', views.TagDelete.as_view(), name='tag_delete'),
    path('urls/', views.UrlsListView.as_view(), name='urls'),
    path('<slug:slug>/detail/', views.DetailUrl.as_view(), name='detail_url'),
    path('<slug:slug>/change/', views.ChangeUrl.as_view(), name='change_url'),
    path('<slug:slug>/delete/', views.DeleteUrl.as_view(), name='delete_url'),
    path('<slug:slug>/', views.RedirectUrl.as_view(), name='redirect_url'),
]
