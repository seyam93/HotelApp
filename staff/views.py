from django.shortcuts import render, get_object_or_404
from .models import Manager
from hotels.models import Hotel

# Create your views here.

# Team list view
def team_list(request, hotel_slug):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    managers = Manager.objects.filter(hotel=hotel)

    return render(request, 'staff/team_list.html', {
        'hotel': hotel,
        'managers': managers
    })

# Team detail view
def team_detail(request, hotel_slug, manager_id):
    hotel = get_object_or_404(Hotel, slug=hotel_slug)
    manager = get_object_or_404(Manager, hotel=hotel, id=manager_id)

    return render(request, 'staff/team_detail.html', {
        'hotel': hotel,
        'manager': manager
    })