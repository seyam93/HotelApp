from django.shortcuts import render, get_object_or_404, HttpResponse, redirect
from .models import (
    Hotel, Room, PageBackground, HotelImage, WelcomeMessage,
    Facility, Review, Amenity, FacilityImage, HotelService, Offer,
    NewsletterSubscriber, HoverSection, HoverImageTab,
    HotelPageBanner, HotelVideoBanner
)
import json 
from django.db.models import Prefetch
from core.models import FAQ
from collections import OrderedDict
from urllib.parse import urlencode
from django.contrib import messages
from datetime import date, timedelta
from django.http import JsonResponse

# Main Hotels Home Page
def home(request):
    hotels = Hotel.objects.all()
    reviews = Review.objects.select_related('hotel').order_by('-created_at')[:6]
    image_banner = HotelPageBanner.objects.filter(hotel=None, page='home').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=None, page='home').first()
    return render(request, 'hotels/home.html', {
        'hotels': hotels,
        'reviews': reviews,
        'banner': image_banner,
        'video_banner': video_banner,
    })

# Single Hotel Home Page 
def hotel_detail(request, slug):
    hotel_qs = Hotel.objects.prefetch_related(
        'rooms', 'hotel_images', 'welcome_messages', 'facilities', 'reviews',
        'hotel_services', 'page_backgrounds')
    hotel = get_object_or_404(hotel_qs, slug=slug)
    section = HoverSection.objects.filter(name=hotel.slug).first()
    tab_items = section.tabs.all() if section else []
    tab_facilities = hotel.facilities.filter(is_active=True, is_featured=True).order_by('type', 'name')
    tab_facility_types = list(OrderedDict.fromkeys(f.type for f in tab_facilities))
    backgrounds_list = [{'src': bg.image.url} for bg in hotel.page_backgrounds.all()]
    backgrounds_json = json.dumps(backgrounds_list)
    faqs = hotel.faqs.all()[:4]
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='home').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='home').first()

    return render(request, 'hotels/hotel_detail.html', {
        'hotel': hotel,
        'rooms': hotel.rooms.all(),
        'hotel_images': hotel.hotel_images.all(),
        'welcome_messages': hotel.welcome_messages.all(),
        'facilities': hotel.facilities.all(),
        'tab_facilities': tab_facilities,
        'tab_facility_types': tab_facility_types,
        'reviews': hotel.reviews.all(),
        'amenity_services': hotel.hotel_services.all()[:6],
        'featured_services': hotel.hotel_services.filter(featured=True)[:3],
        'backgrounds': hotel.page_backgrounds.all(),
        'backgrounds_json': backgrounds_json,
        'banner': image_banner,
        'tab_items': tab_items,
        'faqs': faqs,
        'video_banner': video_banner,
    })

# All Rooms Page For a certain Hotel
def hotel_rooms(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    rooms = hotel.rooms.filter(is_available=True).order_by('display_order').prefetch_related('room_images')
    offers = hotel.offers.filter(is_active=True, is_card=True).order_by('-start_date')[:4]
    today = date.today().strftime('%Y-%m-%d')
    tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='rooms').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='rooms').first()

    return render(request, 'hotels/hotel_rooms.html', {
        'hotel': hotel,
        'rooms': rooms,
        'offers': offers,
        'banner': image_banner,
        'today': today,
        'tomorrow': tomorrow,
        'video_banner': video_banner,
    })

# Room Detail For certain Hotel
def room_detail(request, hotel_slug, room_slug):
    room = get_object_or_404(Room, slug=room_slug, hotel__slug=hotel_slug)
    faqs = room.hotel.faqs.all()[:4]
    image_banner = HotelPageBanner.objects.filter(hotel=room.hotel, page='rooms').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=room.hotel, page='detailroom').first()

    return render(request, 'hotels/room_detail.html', {
        'room': room,
        'hotel': room.hotel,
        'faqs': faqs,
        'banner': image_banner,
        'video_banner': video_banner
    })

# Facilities Page
def hotel_facilities_view(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    featured_active_facilities = Facility.objects.filter(hotel=hotel, is_active=True, is_featured=True).prefetch_related('images').order_by('type', 'name')
    active_facilities = Facility.objects.filter(hotel=hotel, is_active=True).prefetch_related('images').order_by('type', 'name')
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='services').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='services').first()

    return render(request, 'hotels/hotel_facilities.html', {
        'hotel': hotel,
        'tab_facilities': featured_active_facilities,
        'tab_facility_types': list(OrderedDict.fromkeys(f.type for f in featured_active_facilities)),
        'active_facilities': active_facilities,
        'active_facility_types': list(OrderedDict.fromkeys(f.type for f in active_facilities)),
        'banner': image_banner,
        'video_banner': video_banner,
    })

# Offers Page
def offer_list_view(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)

    offers_featured = hotel.offers.filter(is_active=True, is_featured=True).order_by('-start_date')
    offers_card = hotel.offers.filter(is_active=True, is_card=True).order_by('-start_date')[:4]

    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='offers').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='offers').first()

    return render(request, 'hotels/hotel_offers.html', {
        'hotel': hotel,
        'offers_featured': offers_featured,
        'offers_card': offers_card,
        'banner': image_banner,
        'video_banner': video_banner,
    })

# Amenities Page
def hotel_amenities_view(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    services = HotelService.objects.filter(hotel=hotel, featured=True, is_active=True).order_by('title')
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='services').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='services').first()

    return render(request, 'hotels/hotel_amenities.html', {
        'hotel': hotel,
        'services': services,
        'banner': image_banner,
        'video_banner': video_banner
    })

# Image Gallery Page
def image_gallery(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    items = hotel.gallery_items.filter(gallery_type='image', image__isnull=False)
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='images').first()

    return render(request, 'hotels/image_gallery.html', {
        'hotel': hotel,
        'items': items,
        'banner': image_banner
    })

# Video Gallery Page
def video_gallery(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    items = hotel.gallery_items.filter(gallery_type='video')
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='video').first()

    return render(request, 'hotels/video_gallery.html', {
        'hotel': hotel,
        'videos': items,
        'banner': image_banner
    })

# Booking Engine Redirect
def booking_redirect(request):
    if request.method == 'POST':
        base_url = "https://be.synxis.com/"
        chain_id = "29071"
        hotel_id = request.POST.get('hotel_id')

        params = {
            'chain': chain_id,
            'hotel': hotel_id,
            'arrive': request.POST.get('arrival'),
            'depart': request.POST.get('departure'),
            'adult': request.POST.get('adults', 1),
            'child': request.POST.get('children', 0),
        }

        return redirect(f"{base_url}?{urlencode(params)}")

# Newsletter Subscription
def subscribe_newsletter(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if email:
            NewsletterSubscriber.objects.get_or_create(email=email)
            messages.success(request, "Thanks for subscribing!")

    return redirect(request.META.get('HTTP_REFERER', '/'))

# Why Triumph Page
def why_triumph(request):
    image_banner = HotelPageBanner.objects.filter(hotel=None, page='about').first()
    hotels = Hotel.objects.all()
    welcome_message = WelcomeMessage.objects.order_by('created_at').first()

    return render(request, 'hotels/why_triumph.html', {
        'banner': image_banner,
        'hotels': hotels,
        'welcome_message': welcome_message
    })

# Live Search
def live_search(request):
    query = request.GET.get('q', '').strip()
    hotels_data = []
    rooms_data = []

    if query:
        hotels = Hotel.objects.filter(name__icontains=query)[:5]
        rooms = Room.objects.filter(name__icontains=query)[:5]

        hotels_data = [{'name': h.name, 'slug': h.slug} for h in hotels]
        rooms_data = [{'name': r.name, 'hotel_name': r.hotel.name} for r in rooms]

    return JsonResponse({'hotels': hotels_data, 'rooms': rooms_data})

# Custom 404 Page
def custom_404_view(request, exception):
    return render(request, '404.html', status=404)