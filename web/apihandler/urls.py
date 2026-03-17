from django.urls import path
from . import views


urlpatterns = [
    path('events/', views.events_handler, name='home'),
    path('', views.index, name='home'),
]