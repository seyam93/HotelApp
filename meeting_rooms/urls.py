from django.urls import path
from . import views

urlpatterns = [
    path('home/<slug:hotel_slug>/meeting-rooms/', views.meeting_room_list, name='meeting-room-page'),
]