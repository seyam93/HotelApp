from django.urls import path
from . import views

urlpatterns = [
    path('home/<slug:hotel_slug>/contact', views.hotel_contact_view, name='contact-page'),
    path('home/<slug:hotel_slug>/about', views.about_page, name='about-page'),
]
