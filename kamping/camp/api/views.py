from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView

from camp.api.serializers import CampSerializer
from camp.models import Camp


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


class CampUpdateAPIView(UpdateAPIView):
    queryset = Camp.objects.all()
    serializer_class = CampSerializer
    lookup_field = 'slug'