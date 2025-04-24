from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Hotel, Room, HotelImage, WelcomeMessage, Facility, Review, Amenity, HotelService

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/home.html', {'hotels': hotels})

def about(request):
    return render(request, 'hotels/about.html')

# Hotel Detail View & Listing All Rooms in Hotel
# This view will show the details of a specific hotel and list all rooms in that hotel.

def hotel_detail(request, slug):
    hotel = get_object_or_404(
        Hotel.objects.prefetch_related(
            'rooms',
            'hotel_images',
            'welcome_messages',
            'facilities',
            'reviews',
            'hotel_services',
        ),
        slug=slug
    )

    tab_facilities = hotel.facilities.filter(type__in=['restaurant', 'spa', 'pool', 'gym'])
    tab_facility_types = tab_facilities.values_list('type', flat=True).distinct()

    context = {
        'hotel': hotel,
        'rooms': hotel.rooms.all(),
        'hotel_images': hotel.hotel_images.all(),
        'welcome_messages': hotel.welcome_messages.all(),
        'facilities': hotel.facilities.all(),  # All facilities
        'tab_facilities': tab_facilities,      # Only those for tab section
        'tab_facility_types': tab_facility_types,
        'reviews': hotel.reviews.all(),
        'amenity_services': hotel.hotel_services.all()[:6],  # for amenities section (limit to 6)
        'featured_services': hotel.hotel_services.filter(featured=True)[:3],  # for extra prices section
    }

    return render(request, 'hotels/hotel_detail.html', context)

# def hotel_detail(request, slug):
#     hotel = get_object_or_404(Hotel, slug=slug)
#     rooms = hotel.rooms.all()
#     hotel_images = hotel.hotel_images.all()
#     welcome_messages = hotel.welcome_messages.all()
#     facilities = hotel.facilities.all()
#     reviews = hotel.reviews.all()
#     amenities = hotel.amenities.all()
#     hotel_services = hotel.hotel_services.all()
#     context = {
#         'hotel': hotel,
#         'rooms': rooms,
#         'hotel_images': hotel_images,
#         'welcome_messages': welcome_messages,
#         'facilities': facilities,
#         'reviews': reviews,
#         'amenities': amenities,
#         'hotel_services': hotel_services,

#     }
#     return render(request, 'hotels/hotel_detail.html', context)

# Room List View
# This view will list all rooms in the hotel if hotel_slug is provided, otherwise it will list all rooms.

def room_list(request, hotel_slug=None):
    if hotel_slug:
        hotel = get_object_or_404(Hotel, slug=hotel_slug)
        rooms = hotel.rooms.all()
        context = {'rooms': rooms, 'hotel': hotel}
    else:
        rooms = Room.objects.all()
        context = {'rooms': rooms}
    return render(request, 'hotels/rooms.html', context)

def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug)
    return render(request, 'hotels/room_detail.html', {'room': room})

def about(request):
    return render(request, 'hotels/about.html')