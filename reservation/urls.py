from django.urls import path, re_path

from . import views

urlpatterns = [
    path('room/new/', views.room_new_view),
    path('rooms/', views.rooms_view),
]
