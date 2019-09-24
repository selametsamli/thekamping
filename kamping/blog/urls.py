from django.urls import path
from blog import views

urlpatterns = [
    path('post-create', views.post_create, name="post-create"),
    path('post-list', views.post_list, name="post-list"),
    path('post-update/<slug:slug>', views.post_update, name="post-update"),
    path('post-detail/<slug:slug>', views.post_detail, name="post-detail"),

]
