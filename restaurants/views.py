from django.shortcuts import render, get_object_or_404
from .models import Restaurant, RestaurantMenu
from hotels.models import Hotel, HotelPageBanner, HotelVideoBanner

# Restaurant views
def restaurant_list(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='dining').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='dining').first()
    restaurants = hotel.restaurants.all()  # because of related_name="restaurants"
    return render(request, 'restaurants/restaurant_list.html', {
        'hotel': hotel,
        'restaurants': restaurants,
        'banner' : image_banner,
        'video_banner': video_banner,
    })

# Restaurant Detail View
def restaurant_detail(request, hotel_slug, slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    restaurant = get_object_or_404(Restaurant, hotel=hotel, slug=slug)
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='dining').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='detaildining').first()
    return render(request, 'restaurants/restaurant_detail.html', {
        'hotel': hotel,
        'restaurant': restaurant,
        'banner' : image_banner,
        'video_banner': video_banner,
    })

# Restaurant Menu View
def menu_view(request, slug):
    menu = get_object_or_404(RestaurantMenu, slug=slug)
    hotel = menu.restaurant.hotel if hasattr(menu.restaurant, 'hotel') else None  # Optional if there's a link

    return render(request, 'restaurants/restaurant_menus.html', {
        'menu': menu,
        'hotel': hotel  # only if you use it in template
    })