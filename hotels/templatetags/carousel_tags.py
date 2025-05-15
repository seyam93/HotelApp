from django import template
from hotels.models import Hotel

register = template.Library()

@register.inclusion_tag('includes/dynamic_carousel.html')
def render_hotel_carousel():
    hotels = Hotel.objects.filter(image_cover__isnull=False)[:5]
    return {'hotels': hotels}