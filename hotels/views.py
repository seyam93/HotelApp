from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Hotel, Room, PageBackground, HotelImage, WelcomeMessage, Facility, Review, Amenity, FacilityImage, HotelService, Offer
import json 
from django.db.models import Prefetch
from core.models import FAQ
from collections import OrderedDict

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/home.html', {'hotels': hotels})

def about(request):
    return render(request, 'hotels/about.html')

# Hotel Detail View & Listing All Rooms in Hotel
# This view will show the details of a specific hotel and list all rooms in that hotel.
def hotel_detail(request, slug):
    hotel_qs = Hotel.objects.prefetch_related(
        'rooms',
        'hotel_images',
        'welcome_messages',
        'facilities',
        'reviews',
        Prefetch('hotel_services'),
        Prefetch('page_backgrounds', queryset=PageBackground.objects.filter(page='hotel_main')),
    )

    hotel = get_object_or_404(hotel_qs, slug=slug)

    tab_facilities = hotel.facilities.filter(
        is_active=True,
        is_featured=True
    ).order_by('type', 'name')

    tab_facility_types = list(OrderedDict.fromkeys(f.type for f in tab_facilities))

    # Prepare backgrounds for a potential image slider
    backgrounds_list = [{'src': bg.image.url} for bg in hotel.page_backgrounds.all()]
    backgrounds_json = json.dumps(backgrounds_list)

    context = {
        'hotel': hotel,
        'rooms': hotel.rooms.all(),
        'hotel_images': hotel.hotel_images.all(),
        'welcome_messages': hotel.welcome_messages.all(),
        'facilities': hotel.facilities.all(),  # full list if needed elsewhere
        'tab_facilities': tab_facilities,      # only active & featured (for tabs)
        'tab_facility_types': tab_facility_types,
        'reviews': hotel.reviews.all(),
        'amenity_services': hotel.hotel_services.all()[:6],
        'featured_services': hotel.hotel_services.filter(featured=True)[:3],
        'backgrounds': hotel.page_backgrounds.all(),
        'backgrounds_json': backgrounds_json,
    }

    return render(request, 'hotels/hotel_detail.html', context)

# Rooms List View
# This view will list all available rooms in a specific hotel.
def hotel_rooms(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    rooms = hotel.rooms.filter(is_available=True).prefetch_related('room_images')

    context = {
        'hotel': hotel,
        'rooms': rooms,
    }
    return render(request, 'hotels/hotel_rooms.html', context)

# Room Detail View
# This view will show the details of a specific room in a hotel.
def room_detail(request, hotel_slug, room_slug):
    room = get_object_or_404(Room, slug=room_slug, hotel__slug=hotel_slug)
    hotel = room.hotel
    faqs = hotel.faqs.all()[:4]

    context = {
        'room': room,
        'hotel': hotel,  # ✅ Include hotel for slug usage in templates
        'faqs': faqs,
    }
    return render(request, 'hotels/room_detail.html', context)

# facility list view
def hotel_facilities_view(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)

    featured_active_facilities = Facility.objects.filter(
        hotel=hotel, is_active=True, is_featured=True
    ).prefetch_related('images').order_by('type', 'name')

    active_facilities = Facility.objects.filter(
        hotel=hotel, is_active=True
    ).prefetch_related('images').order_by('type', 'name')

    context = {
        'hotel': hotel,
        'tab_facilities': featured_active_facilities,
        'tab_facility_types': list(OrderedDict.fromkeys(f.type for f in featured_active_facilities)),
        'active_facilities': active_facilities,
        'active_facility_types': list(OrderedDict.fromkeys(f.type for f in active_facilities)),
    }
    return render(request, 'hotels/hotel_facilities.html', context)

# Offer List View 
def offer_list_view(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    offers = hotel.offers.filter(is_active=True).order_by('-start_date')

    context = {
        'hotel': hotel,
        'offers': offers,
    }
    return render(request, 'hotels/hotel_offers.html', context)


# def hotel_facilities_view(request, hotel_slug):
#     hotel = get_object_or_404(Hotel, slug=hotel_slug)

#     # 🔼 Upper Section (Featured & Active)
#     featured_active_facilities = Facility.objects.filter(
#         hotel=hotel,
#         is_active=True,
#         is_featured=True
#     ).prefetch_related('images').order_by('type', 'name')

#     # 🔽 Lower Section (All Active, even if not featured)
#     active_facilities = Facility.objects.filter(
#         hotel=hotel,
#         is_active=True
#     ).prefetch_related('images').order_by('type', 'name')

#     context = {
#         'hotel': hotel,
#         # For upper section (featured + active tabs)
#         'tab_facilities': featured_active_facilities,
#         'tab_facility_types': list({f.type for f in featured_active_facilities}),
        
#         # For lower section (all active facilities grid)
#         'active_facilities': active_facilities,
#         'active_facility_types': list({f.type for f in active_facilities}),
#     }
#     return render(request, 'hotels/hotel_facilities.html', context)

# Hotel Services ( Amenities For Hotel ) View
def hotel_amenities_view(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    
    services = HotelService.objects.filter(
        hotel=hotel,
        featured=True,
        is_active=True
    ).order_by('title')

    context = {
        'hotel': hotel,
        'services': services,
    }
    return render(request, 'hotels/hotel_amenities.html', context)

# def hotel_detail(request, slug):
#     hotel = get_object_or_404(
#         Hotel.objects.prefetch_related(
#             'rooms',
#             'hotel_images',
#             'welcome_messages',
#             'facilities',
#             'reviews',
#             'hotel_services',
#             'backgrounds',
#         ),
#         slug=slug
#     )

#     tab_facilities = hotel.facilities.filter(type__in=['restaurant', 'spa', 'pool', 'gym'])
#     tab_facility_types = tab_facilities.values_list('type', flat=True).distinct()

#     context = {
#         'hotel': hotel,
#         'rooms': hotel.rooms.all(),
#         'hotel_images': hotel.hotel_images.all(),
#         'welcome_messages': hotel.welcome_messages.all(),
#         'facilities': hotel.facilities.all(),  # All facilities
#         'tab_facilities': tab_facilities,      # Only those for tab section
#         'tab_facility_types': tab_facility_types,
#         'reviews': hotel.reviews.all(),
#         'amenity_services': hotel.hotel_services.all()[:6],  # for amenities section (limit to 6)
#         'featured_services': hotel.hotel_services.filter(featured=True)[:3],  # for extra prices section
#         'backgrounds': hotel.backgrounds.all(), # for background images
#     }

#     return render(request, 'hotels/hotel_detail.html', context)

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

# def room_list(request, hotel_slug=None):
#     if hotel_slug:
#         hotel = get_object_or_404(Hotel, slug=hotel_slug)
#         rooms = hotel.rooms.all()
#         context = {'rooms': rooms, 'hotel': hotel}
#     else:
#         rooms = Room.objects.all()
#         context = {'rooms': rooms}
#     return render(request, 'hotels/rooms.html', context)

# def room_detail(request, slug):
#     room = get_object_or_404(Room, slug=slug)
#     return render(request, 'hotels/room_detail.html', {'room': room})

def about(request):
    return render(request, 'hotels/about.html')