from django.contrib import admin
from blog.models import Blog


# Register your models here.


class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_date')


admin.site.register(Blog, BlogAdmin)
