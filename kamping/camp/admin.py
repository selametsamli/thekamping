from django.contrib import admin

# Register your models here.
from camp.models import Camp, CampParticipants, Photo, Comment, Feedback


class CampAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'status')


class CampParticipantsAdmin(admin.ModelAdmin):
    list_display = ('camp', 'user', 'created_date')


class PhotosAdmin(admin.ModelAdmin):
    list_display = ('camp',)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('icerik', 'user', 'comment_date')


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'camp', 'point')


admin.site.register(Camp, CampAdmin)
admin.site.register(CampParticipants, CampParticipantsAdmin)
admin.site.register(Photo, PhotosAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Feedback, FeedbackAdmin)
