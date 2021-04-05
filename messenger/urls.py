from django.urls import path
from . import views


urlpatterns = [
    path('', views.DialogListView.as_view(), name='dialog_list'),
    path('dialog/<str:username>/', views.DialogView.as_view(), name='dialog'),
]