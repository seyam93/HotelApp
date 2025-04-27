from django.shortcuts import render, get_object_or_404
from .models import Restaurant
from hotels.models import Hotel

# Restaurant views
def restaurant_list(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    restaurants = hotel.restaurants.all()  # because of related_name="restaurants"
    return render(request, 'restaurants/restaurant_list.html', {
        'hotel': hotel,
        'restaurants': restaurants
    })

def restaurant_detail(request, hotel_slug, slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    restaurant = get_object_or_404(Restaurant, hotel=hotel, slug=slug)
    return render(request, 'restaurants/restaurant_detail.html', {
        'hotel': hotel,
        'restaurant': restaurant
    })