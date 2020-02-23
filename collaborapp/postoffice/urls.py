from django.urls import path, include
import postoffice.views

urlpatterns = [
    path('', postoffice.views.home, name='postoffice_home'),
]
