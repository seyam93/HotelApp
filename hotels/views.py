from django.shortcuts import render, get_object_or_404
from .models import Hotel, Room

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/home.html', {'hotels': hotels})

def about(request):
    return render(request, 'hotels/about.html')

def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel})

def room_list(request):
    rooms = Room.objects.all()
    return render(request, 'hotels/rooms.html', {'rooms': rooms})

def room_detail(request):
    # Dummy test data
    room = {
        'name': 'Ocean View Suite',
        'description': 'A beautiful suite with a view of the sea.',
        'price': 350
    }
    return render(request, 'hotels/rooms_detail.html', {'room': room})

