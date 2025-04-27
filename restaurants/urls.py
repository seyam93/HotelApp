from django.urls import path
from . import views

urlpatterns = [
    path('<slug:hotel_slug>/restaurants/', views.restaurant_list, name='restaurant-list'),
    path('<slug:hotel_slug>/restaurants/<slug:slug>/', views.restaurant_detail, name='restaurant-detail'),
]