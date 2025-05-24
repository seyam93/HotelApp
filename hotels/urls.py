from django.urls import path
from . import views
from django.views.generic import TemplateView
from .views import booking_redirect

urlpatterns = [
    path('', views.home, name='home-page'),
    path('home/<slug:slug>/', views.hotel_detail, name='hotel-detail'),
    path('home/<slug:hotel_slug>/rooms/', views.hotel_rooms, name='hotel-rooms'),
    path('home/<slug:hotel_slug>/rooms/<slug:room_slug>/', views.room_detail, name='room-detail'), 
    path('home/<slug:hotel_slug>/facilities/', views.hotel_facilities_view, name='hotel-facilities-page'),
    path('home/<slug:hotel_slug>/amenities/', views.hotel_amenities_view, name='hotel-amenities-page'),
    path('home/<slug:hotel_slug>/offers/', views.offer_list_view, name='offer-page'),
    path('home/<slug:hotel_slug>/image-gallery/', views.image_gallery, name='image-gallery-page'),
    path('home/<slug:hotel_slug>/video-gallery/', views.video_gallery, name='video-gallery-page'),
    path('why-triumph/', views.why_triumph, name='why-triumph'),
    path('booking/redirect/', booking_redirect, name='booking-redirect'),
    path('subscribe/', views.subscribe_newsletter, name='subscribe-newsletter'),
]