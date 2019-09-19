from django.urls import path
from camp import views

urlpatterns = [
    path('camp-create', views.camp_create, name="camp-create"),
    path('basic-upload/<slug:slug>', views.upload_photo, name="basic-upload"),
    path('camp-update/<slug:slug>', views.camp_update, name="camp-update"),
    path('camp-detail/<slug:slug>', views.camp_detail, name="camp-detail"),
    path('camp-remove/<slug:slug>', views.camp_remove, name="camp-remove"),
    path('camp-add-or-remove/<slug:slug>', views.add_or_remove_camp, name="camp-add-or-remove"),

]
