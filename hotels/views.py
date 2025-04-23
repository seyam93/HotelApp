from django.shortcuts import render, get_object_or_404, HttpResponse
from .models import Hotel, Room

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/home.html', {'hotels': hotels})

def about(request):
    return render(request, 'hotels/about.html')

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

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hotels/rooms.html', {'rooms': rooms})

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    return render(request, 'hotels/room-detail.html', {'room': room})