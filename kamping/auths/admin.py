from django.contrib import admin

# Register your models here.
from auths.models import UserProfile

admin.site.register(UserProfile)
