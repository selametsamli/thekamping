from django.contrib import admin

# Register your models here.
from camp.models import Camp, CampParticipants, Photo


class CampAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status')


class CampParticipantsAdmin(admin.ModelAdmin):
    list_display = ('camp', 'user', 'created_date')


class PhotosAdmin(admin.ModelAdmin):
    list_display = ('camp',)


admin.site.register(Camp, CampAdmin)
admin.site.register(CampParticipants, CampParticipantsAdmin)
admin.site.register(Photo, PhotosAdmin)
