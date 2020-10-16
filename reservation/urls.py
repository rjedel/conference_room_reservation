from django.urls import path, re_path

from . import views

urlpatterns = [
    path('room/new/', views.room_new_view),
    path('rooms/', views.rooms_view),
    path('room/delete/<int:id>/', views.room_delete_by_id_view),
    path('room/modify/<int:id>/', views.room_modify_by_id_view),
]
