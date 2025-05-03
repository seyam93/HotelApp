from django.shortcuts import render, get_object_or_404
from .models import MeetingRoom
from hotels.models import Hotel

# List of meeting rooms for a specific hotel
def meeting_room_list(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    meeting_rooms = hotel.meeting_rooms.filter(available=True).prefetch_related('amenities', 'seating_arrangements', 'images')
    return render(request, 'meeting_rooms/meeting_room_list.html', {
        'hotel': hotel,
        'meeting_rooms': meeting_rooms
    })

# Detail of a single meeting room for a specific hotel
# def meeting_room_detail(request, hotel_slug, room_slug):
#     hotel = get_object_or_404(Hotel, slug=hotel_slug)
#     meeting_room = get_object_or_404(
#         MeetingRoom.objects.prefetch_related('amenities', 'seating_arrangements', 'images'),
#         hotel=hotel,
#         slug=room_slug
#     )
#     return render(request, 'meeting_rooms/meeting_room_detail.html', {
#         'hotel': hotel,
#         'meeting_room': meeting_room
#     })