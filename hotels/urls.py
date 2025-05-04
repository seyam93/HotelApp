from django.urls import path
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.home, name='home-page'),
    path('about', views.about, name='about-page'),
    path('home/<slug:slug>/', views.hotel_detail, name='hotel-detail'),
    path('home/<slug:hotel_slug>/rooms/', views.hotel_rooms, name='hotel-rooms'),
    path('home/<slug:hotel_slug>/rooms/<slug:room_slug>/', views.room_detail, name='room-detail'), 
    path('home/<slug:hotel_slug>/facilities/', views.hotel_facilities_view, name='hotel-facilities-page'),
    path('home/<slug:hotel_slug>/amenities/', views.hotel_amenities_view, name='hotel-amenities-page'),
    path('home/<slug:hotel_slug>/offers/', views.offer_list_view, name='offer-page'),
    path('home/<slug:hotel_slug>/image-gallery/', views.image_gallery, name='image-gallery-page'),
    path('home/<slug:hotel_slug>/video-gallery/', views.video_gallery, name='video-gallery-page'),
    path('test-gallery/', TemplateView.as_view(template_name='hotels/test_gallery.html')),
]