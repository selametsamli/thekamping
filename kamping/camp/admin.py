from django.contrib import admin

# Register your models here.
from camp.models import Camp, CampParticipants

admin.site.register(Camp)
admin.site.register(CampParticipants)
