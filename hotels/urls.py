from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('about', views.about, name='about-page'),
    # path('rooms', views.room_list, name='rooms'),
    path('home/<slug:slug>/', views.hotel_detail, name='hotel-detail'),
    path('home/<slug:slug>/rooms/', views.hotel_rooms, name='hotel-rooms'),
    path('home/<slug:hotel_slug>/rooms/<slug:room_slug>/', views.room_detail, name='room-detail'), 
    path('home/<slug:hotel_slug>/facilities/', views.hotel_facilities_view, name='hotel-facilities-page'),
]
