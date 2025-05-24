from django.shortcuts import render, get_object_or_404
from .models import MeetingRoom
from hotels.models import Hotel
from common.utils import get_page_banner

# Meeting Room List View
def meeting_room_list(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    meeting_rooms = hotel.meeting_rooms.filter(available=True).prefetch_related('amenities', 'seating_arrangements', 'images')
    banner = get_page_banner(hotel, 'meeting')  # dynamically fetch "meeting" page banner
    return render(request, 'meeting_rooms/meeting_room_list.html', {
        'hotel': hotel,
        'meeting_rooms': meeting_rooms,
        'banner': banner,
    })

# Wedding Meeting Rooms View
def wedding_meeting_rooms(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    meeting_rooms = hotel.meeting_rooms.filter(can_have_weeding=True, available=True).prefetch_related('amenities', 'seating_arrangements', 'images')
    banner = get_page_banner(hotel, 'wedding')  # dynamically fetch "wedding" page banner
    return render(request, 'meeting_rooms/wedding_meeting_rooms.html', {
        'hotel': hotel,
        'meeting_rooms': meeting_rooms,
        'banner': banner,
    })
