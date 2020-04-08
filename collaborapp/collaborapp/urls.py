"""collaborapp URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
import notes.views, birthdays.views, home.views, postoffice.views
import postoffice.urls
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', home.views.go_home, name='go_home'), 
    path('live/', admin.site.urls),
    path(r'birthdays/<birthday_person>/<age>/', birthdays.views.show_card, name='show_birthday_card'),
    path('signup/', home.views.signup),
    path('notes/', notes.views.home),
    path('login/', home.views.login_user),
    path('logout/', home.views.logout_user),
    path('postoffice/', include('postoffice.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) 
