from django.urls import path
from camp import views

urlpatterns = [
    path('camp-create', views.camp_create, name="camp-create"),
    path('camp-update/<slug:slug>', views.camp_update, name="camp-update"),

]
