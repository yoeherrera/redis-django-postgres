from django.urls import path
from . import views

app_name = 'chat'  # Use a namespace to avoid conflicts
urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login_view'),
    path('room/', views.room, name='room'),
    path('', views.index, name='index'),
]
