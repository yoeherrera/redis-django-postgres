# chat/urls.py

from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),  # Add this line
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('room/', views.room, name='room'),
]
