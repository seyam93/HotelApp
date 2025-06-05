from django.urls import path
from . import views

urlpatterns = [
    path('home/<slug:hotel_slug>/restaurants/', views.restaurant_list, name='restaurant-list'),
    path('home/<slug:hotel_slug>/restaurants/<slug:slug>/', views.restaurant_detail, name='restaurant-detail'),
    path('menus/<slug:slug>/', views.menu_view, name='restaurant-menu'),
]