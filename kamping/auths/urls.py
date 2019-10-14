from django.conf.urls import url
from django.urls import path, include
from auths import views
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', include('django.contrib.auth.urls')),

    path('login-user/', views.user_login, name="user-login"),
    path('register/', views.user_register, name="user-register"),
    path('logout-user/', views.user_logout, name="user-logout"),
    path('user-profile-update/', views.profile_update, name="user-profile-update"),
    path('<str:username>/', views.user_profile, name="user-profile"),

    #email verification
    path('activate/<slug:uidb64>/<slug:token>/', views.activate, name='activate'),
    path('email-verification/', views.email_verification_page, name='email-verification'),
    path('verification-mail-send/', views.verification_mail_send, name='verification-mail-send'),

    #password reset
    path('password_reset/', auth_views.PasswordResetView, name="password-reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView, name="password-reset_done"),
    path('reset/<slug:uidb64>/<slug:token>/', auth_views.PasswordResetConfirmView, name='password-reset-confirm'),
    path('password_reset_confirm/', auth_views.PasswordResetCompleteView, name="password-reset-complate"),

]
