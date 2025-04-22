from django.shortcuts import render, get_object_or_404
from .models import Hotel

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'hotels/home.html', {'hotels': hotels})

def about(request):
    return render(request, 'hotels/about.html')

def hotel_detail(request, slug):
    hotel = get_object_or_404(Hotel, slug=slug)
    return render(request, 'hotels/hotel_detail.html', {'hotel': hotel})

