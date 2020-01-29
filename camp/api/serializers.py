from rest_framework import serializers

from camp.models import Camp, Photo


class CampSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camp
        fields = [
            'user', 'title', 'content', 'created_date', 'starter_time', 'starter_date', 'cover_photo', 'size',
            'location', 'status', 'slug'

        ]


class CampCreateUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Camp
        fields = [
            "title", "content", "starter_date", 'starter_time', 'location', 'size'
        ]


class CampCreatePictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Photo

        fields = [
            'file'
        ]
