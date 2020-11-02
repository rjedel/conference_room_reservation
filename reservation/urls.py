from django.urls import path

from . import views

urlpatterns = [
    path('room/new/', views.room_new_view, name="room-new"),
    path('', views.rooms_view, name="room-table"),
    path('room/delete/<int:room_id>/', views.room_delete_by_id_view, name="room-delete"),
    path('room/modify/<int:room_id>/', views.room_modify_by_id_view, name="room-modify"),
    path('room/reserve/<int:room_id>/', views.room_reserve_by_id_view, name="room-reserve"),
    path('room/details/<int:room_id>/', views.room_details_view, name="room-details"),
    path('search/', views.search_view, name="room-search"),
    path('about/', views.about_view, name="room-about"),
]
