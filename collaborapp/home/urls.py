from django.urls import path
from . import views


app_name = 'home'

urlpatterns = [
    path('', views.go_home, name='go_home'),
    path('login/', views.login_user),
    path('logout/', views.logout_user),
]