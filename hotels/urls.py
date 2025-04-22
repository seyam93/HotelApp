from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('about', views.about, name='about-page'),
    path('rooms', views.room_list, name='room_list'),
    path('home/rooms-detail', views.room_detail, name='room_detail'),
    path('<slug:slug>/', views.hotel_detail, name='hotel_detail'),  
]