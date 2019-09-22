from django.contrib import admin

# Register your models here.
from camp.models import Camp, CampParticipants, Photo, Comment


class CampAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status')


class CampParticipantsAdmin(admin.ModelAdmin):
    list_display = ('camp', 'user', 'created_date')


class PhotosAdmin(admin.ModelAdmin):
    list_display = ('camp',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('icerik', 'user', 'comment_date')


admin.site.register(Camp, CampAdmin)
admin.site.register(CampParticipants, CampParticipantsAdmin)
admin.site.register(Photo, PhotosAdmin)
admin.site.register(Comment, CommentAdmin)
