from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static

from kamping import settings
from camp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.camp_list, name="index"),
    path('camp/', include('camp.urls')),

]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
