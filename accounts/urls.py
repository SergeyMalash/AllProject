from django.urls import path

from accounts import views

urlpatterns = [
    path('', views.DetailAccount.as_view(), name='detail_account'),
    path('register/', views.RegisterAccountView.as_view(), name='register_account'),
    path('register/done/', views.RegisterAccountDoneView.as_view(), name='register_done'),
    path('activation/<str:username>.<str:token>/', views.ActivationAccountView.as_view(), name='activation_account'),
    path('login/', views.LoginAccountView.as_view(), name='login_account'),
    path('logout/', views.LogoutAccountView.as_view(), name='logout_account'),
    path('change/', views.ChangeAccountView.as_view(), name='change_account'),
    path('delete/', views.DeleteAccountView.as_view(), name='delete_account'),
    path('password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('password/reset/', views.ResetPasswordView.as_view(), name='reset_password'),
    path('password/reset/done/', views.ResetPasswordDoneView.as_view(), name='password_reset_done'),
    path('password/reset/confirm/<uidb64>.<token>/', views.ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    path('password/reset/complete/', views.ResetPasswordCompleteView.as_view(), name='password_reset_complete'),
]