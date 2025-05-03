from django.urls import path
from . import views

urlpatterns = [
    path('home/<slug:hotel_slug>/events/', views.hotel_event_list, name='hotel-event-page'),
]