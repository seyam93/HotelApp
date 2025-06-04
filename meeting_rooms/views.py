from django.shortcuts import render, get_object_or_404
from .models import MeetingRoom
from hotels.models import Hotel, HotelPageBanner, HotelVideoBanner

# Meeting Room List View
def meeting_room_list(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    meeting_rooms = hotel.meeting_rooms.filter(available=True).prefetch_related('amenities', 'seating_arrangements', 'images')
    
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='meeting').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='meeting').first()

    return render(request, 'meeting_rooms/meeting_room_list.html', {
        'hotel': hotel,
        'meeting_rooms': meeting_rooms,
        'banner': image_banner,
        'video_banner': video_banner,
    })

# Wedding Meeting Rooms View
def wedding_meeting_rooms(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    meeting_rooms = hotel.meeting_rooms.filter(can_have_weeding=True, available=True).prefetch_related('amenities', 'seating_arrangements', 'images')
    image_banner = HotelPageBanner.objects.filter(hotel=hotel, page='wedding').first()
    video_banner = HotelVideoBanner.objects.filter(hotel=hotel, page='wedding').first()
    return render(request, 'meeting_rooms/wedding_meeting_rooms.html', {
        'hotel': hotel,
        'meeting_rooms': meeting_rooms,
        'banner': image_banner,
        'video_banner': video_banner,
    })
