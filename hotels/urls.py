from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('about', views.about, name='about-page'),
    path('rooms', views.room_list, name='rooms'),
    path('rooms/<int:room_id>/', views.room_detail, name='room_detail'),
    path('<slug:hotel_slug>/rooms/', views.room_list, name='rooms_by_hotel'),
    path('<slug:slug>/', views.hotel_detail, name='hotel_detail'),  
]
