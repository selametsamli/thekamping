from django.urls import path
from camp import views

urlpatterns = [
    path('camp-create', views.camp_create, name="camp-create"),

]
