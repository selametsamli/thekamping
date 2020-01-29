from django.urls import path
from camp.api.views import (
    CampListAPIView,
    CampDetailAPIView,
    CampUpdateAPIView,
    CampDeleteAPIView,
    CampCreateAPIView,
    CampCreatePictureAPIView)

urlpatterns = [
    path('camp-list/', CampListAPIView.as_view(), name='api-camp-list'),
    path('camp-detail/<slug>', CampDetailAPIView.as_view(), name='api-camp-detail'),
    path('camp-update/<slug>', CampUpdateAPIView.as_view(), name='api-camp-update'),
    path('camp-delete/<slug>', CampDeleteAPIView.as_view(), name='api-camp-delete'),
    path('camp-create/', CampCreateAPIView.as_view(), name='api-camp-create'),
    path('camp-create-picture/<slug>', CampCreatePictureAPIView.as_view(), name='api-camp-create-picture'),

]
