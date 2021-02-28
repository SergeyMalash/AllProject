from django.urls import path
from . import views


urlpatterns = [
    path('', views.FindChatView.as_view(), name='find_chat'),
]
