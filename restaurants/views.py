from django.shortcuts import render, get_object_or_404
from .models import Restaurant
from hotels.models import Hotel
from common.utils import get_page_banner, get_video_banner

# Restaurant views
def restaurant_list(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    banner = get_page_banner(hotel, 'dining')
    video_banner = get_video_banner(hotel, 'dining')
    restaurants = hotel.restaurants.all()  # because of related_name="restaurants"
    return render(request, 'restaurants/restaurant_list.html', {
        'hotel': hotel,
        'restaurants': restaurants,
        'banner' : banner,
        'video_banner': video_banner,
    })

# Restaurant Detail View
def restaurant_detail(request, hotel_slug, slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    restaurant = get_object_or_404(Restaurant, hotel=hotel, slug=slug)
    banner = get_page_banner(hotel, 'dining')
    video_banner = get_video_banner(hotel, 'detaildining')
    return render(request, 'restaurants/restaurant_detail.html', {
        'hotel': hotel,
        'restaurant': restaurant,
        'banner' : banner,
        'video_banner': video_banner,
    })