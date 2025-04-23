from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Hotel, Room

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/home.html', {'hotels': hotels})

def about(request):
    return render(request, 'hotels/about.html')

# Hotel Detail View & Listing All Rooms in Hotel
# This view will show the details of a specific hotel and list all rooms in that hotel.

def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    rooms = hotel.rooms.all()
    hotel_images = hotel.hotel_images.all()
    welcome_messages = hotel.welcome_messages.all()
    facilities = hotel.facilities.all()
    context = {
        'hotel': hotel,
        'rooms': rooms,
        'hotel_images': hotel_images,
        'welcome_messages': welcome_messages,
        'facilities': facilities,
    }
    return render(request, 'hotels/hotel_detail.html', context)

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

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    return render(request, 'hotels/room-detail.html', {'room': room})

def about(request):
    return render(request, 'hotels/about.html')