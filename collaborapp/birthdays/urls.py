from django.urls import path
from . import views


urlpatterns = [
    path(r'<birthday_person>/<age>/', views.show_card, name='show_birthday_card'),
]