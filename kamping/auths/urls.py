from django.urls import path
from auths import views

urlpatterns = [
    path('login/', views.user_login, name="user-login"),
    path('register/', views.user_register, name="user-register"),
    path('logout/', views.user_logout, name="user-logout"),
    path('user-profile-update/', views.profile_update, name="user-profile-update"),
    path('<str:username>/', views.user_profile, name="user-profile"),

]
