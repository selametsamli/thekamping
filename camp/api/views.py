from django.shortcuts import get_object_or_404
from rest_framework.generics import (
    ListAPIView,
    RetrieveAPIView,
    DestroyAPIView,
    CreateAPIView,

    RetrieveUpdateAPIView)

from camp.api.permissions import IsOwner, UserIsVerified
from camp.api.serializers import (
    CampSerializer,
    CampCreateUpdateSerializer
)

from rest_framework.permissions import (
    IsAuthenticated,

    IsAdminUser)

from datetime import datetime, timedelta
from camp.models import Camp
from camp.tasks import camp_change_status


class CampListAPIView(ListAPIView):
    queryset = Camp.objects.all()
    serializer_class = CampSerializer


class CampDetailAPIView(RetrieveAPIView):
    queryset = Camp.objects.all()
    serializer_class = CampSerializer
    lookup_field = 'slug'


class CampDeleteAPIView(DestroyAPIView):
    queryset = Camp.objects.all()
    serializer_class = CampSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]


class CampUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Camp.objects.all()
    serializer_class = CampCreateUpdateSerializer
    lookup_field = 'slug'
    permission_classes = [IsOwner]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)


class CampCreateAPIView(CreateAPIView):
    queryset = Camp.objects.all()
    serializer_class = CampCreateUpdateSerializer
    permission_classes = [IsAuthenticated, UserIsVerified]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        camp = get_object_or_404(Camp, title=serializer.data['title'])
        date_time_obj = self.return_data_time_obj(serializer)

        slug = camp.slug
        user = camp.user.username
        camp_change_status.apply_async(kwargs={'slug': slug, 'user': user}, eta=date_time_obj)

    def return_data_time_obj(self, serializer):
        starter_date = str(serializer.data['starter_date']) + " " + str(serializer.data['starter_time']) + '.0'
        date_time_obj = datetime.strptime(starter_date, '%Y-%m-%d %H:%M:%S.%f')
        date_time_obj = date_time_obj - timedelta(hours=3)
        return date_time_obj
