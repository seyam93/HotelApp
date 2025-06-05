# hotels/sitemaps.py
from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Hotel

class HotelSitemap(Sitemap):
    changefreq = "weekly"
    priority = 0.8

    def items(self):
        return Hotel.objects.all()

    def location(self, obj):
        return reverse('hotel-detail', args=[obj.slug])