from django.urls import path
from blog import views

urlpatterns = [
    path('post-create', views.post_create, name="post-create"),

]
