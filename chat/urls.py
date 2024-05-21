from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.login, name='login'),
    path('room/', views.index, name='room'),
]
