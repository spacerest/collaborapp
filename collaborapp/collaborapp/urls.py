"""collaborapp URL Configuration"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', include('home.urls')),  # main home page
    path('notes/', include('notes.urls')),
    path('birthdays/', include('birthdays.urls')),
    path('postoffice/', include('postoffice.urls')),
    path('live/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
