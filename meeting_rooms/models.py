from django.db import models
from hotels.models import Hotel 
from PIL import Image
from io import BytesIO
from django.core.files.base import ContentFile 
from django.utils.text import slugify
from django.utils.html import format_html
import qrcode
import base64
from django.urls import reverse
from django.utils.safestring import mark_safe
from django.conf import settings
from utils.qr_code_generator import generate_qr_code 


class MeetingRoomAmenity(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Meeting Room Amenity'
        verbose_name_plural = 'Meeting Room Amenities'

class SeatingArrangement(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    capacity = models.PositiveIntegerField(null=True, blank=True)
    image = models.ImageField(upload_to='meeting_room_seating_images/', null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Seating Arrangement'
        verbose_name_plural = 'Seating Arrangements'


class MeetingRoom(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="meeting_rooms", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(null=True, blank=True)
    slug = models.SlugField(blank=True, unique=True,editable=False)
    area = models.PositiveIntegerField(default=30, null=True, blank=True, help_text="Area in square meters")
    description = models.TextField(null=True, blank=True)
    image_cover = models.ImageField(upload_to='meeting_room_images/', null=True, blank=True)
    available = models.BooleanField(default=True)
    amenities = models.ManyToManyField(MeetingRoomAmenity, related_name="meeting_rooms", blank=True)
    seating_arrangements = models.ManyToManyField(SeatingArrangement, related_name="meeting_rooms", blank=True)
    can_have_weeding = models.BooleanField(default=False)
    wedding_brochure = models.FileField(upload_to='wedding_brochures/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.hotel.name} (Capacity: {self.capacity}, Area: {self.area} m²)"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class MeetingRoomImages(models.Model):
    meeting_room = models.ForeignKey(MeetingRoom, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='meeting_room_images/')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.meeting_room.name}"

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            target_size = (1280, 720)
            if img.size != target_size:
                img = img.convert("RGB")  # Handle RGBA
                img = img.resize(target_size, Image.LANCZOS)
                img_io = BytesIO()
                img.save(img_io, format='JPEG')
                self.image.save(self.image.name, ContentFile(img_io.getvalue()), save=False)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Meeting Room Image'
        verbose_name_plural = 'Meeting Room Images'

# Meeting Room Brochure Model
class EventBrochure(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE, related_name="event_brochures")
    title = models.CharField(max_length=255)

    corporate_pdf = models.FileField(upload_to="event_brochures/", blank=True, null=True)
    wedding_pdf = models.FileField(upload_to="event_brochures/", blank=True, null=True)
    bofeh_pdf = models.FileField(upload_to="event_brochures/", blank=True, null=True)
    setmenu_pdf = models.FileField(upload_to="event_brochures/", blank=True, null=True)
    offers_pdf = models.FileField(upload_to="event_brochures/", blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.title}"

    def get_absolute_url(self):
        return reverse('event-brochures', kwargs={'hotel_slug': self.hotel.slug})
    
    def qr_code_preview(self):
        full_url = f"{settings.SITE_DOMAIN}{self.get_absolute_url()}"
        qr_data_uri = generate_qr_code(full_url)
        return mark_safe(f'<img src="{qr_data_uri}" width="150" height="150" />')
    
    qr_code_preview.short_description = "QR Code"
# The MeetingRoom model represents a meeting room in a hotel, with fields for its name, capacity, area, description, image, availability, amenities, seating arrangements, and wedding brochure.
# The MeetingRoomAmenity model represents amenities available in meeting rooms, while the SeatingArrangement model represents different seating arrangements with their respective capacities and images.