from django.conf.urls import url
from django.urls import path
from auths import views

urlpatterns = [
    path('email-verification/', views.email_verification_page, name='email-verification'),
    path('verification-mail-send/', views.verification_mail_send, name='verification-mail-send'),
    path('login/', views.user_login, name="user-login"),
    path('register/', views.user_register, name="user-register"),
    path('logout/', views.user_logout, name="user-logout"),
    path('user-profile-update/', views.profile_update, name="user-profile-update"),
    path('<str:username>/', views.user_profile, name="user-profile"),

    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),

]
