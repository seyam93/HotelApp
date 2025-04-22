from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home-page'),
    path('about', views.about, name='about-page'),
    path('<slug:slug>/', views.hotel_detail, name='hotel_detail'),  
]