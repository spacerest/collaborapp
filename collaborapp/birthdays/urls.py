from django.urls import path
from . import views

app_name = 'birthdays'

urlpatterns = [
    path(r'', views.home, name='home'),
    path(r'<birthday_person>/<birthday_gifter>/<age>/', views.show_card, name='show_birthday_card'),
]
