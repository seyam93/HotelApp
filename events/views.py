from django.shortcuts import render, get_object_or_404
from .models import Event
from hotels.models import Hotel

# List events for a specific hotel
def hotel_event_list(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    events = hotel.events.filter(is_active=True).order_by('-start_date')
    
    return render(request, 'events/hotel_event_list.html', {
        'hotel': hotel,
        'events': events,
    })