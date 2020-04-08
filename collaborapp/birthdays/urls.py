from django.urls import path
from . import views

app_name='birthday'

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'<birthday_person>/<age>/', views.show_card, name='show_birthday_card'),
]
