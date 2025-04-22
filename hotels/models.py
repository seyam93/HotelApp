from django.db import models
from django.template.defaultfilters import slugify

# Hotel Models
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    location = models.CharField(max_length=500, default="")
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    image_cover = models.ImageField(upload_to='hotel_covers/', null=True, blank=True)
    fact_sheet = models.FileField(upload_to='hotel_fact_sheets/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="hotel_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.hotel.name}"


class WelcomeMessage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="welcome_messages", on_delete=models.CASCADE)
    title = models.CharField(max_length=255, blank=True, null=True)
    description = models.TextField(default="Welcome to our hotel.")
    image = models.ImageField(upload_to='welcome_messages/', null=True, blank=True)
    message = models.TextField(default="We’re happy to have you with us.")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.message[:50]

    
#Rooms - Features - Specifications Models
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="rooms", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    number_of_beds = models.PositiveIntegerField(default=1)
    area = models.FloatField(help_text="Area in square meters")
    is_suit = models.BooleanField(default=False)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    is_available = models.BooleanField(default=True)
    image_cover = models.ImageField(upload_to='room_covers/', null=True, blank=True)
    check_in_notes = models.TextField(blank=True)
    check_out_notes = models.TextField(blank=True)
    special_check_in_instructions = models.TextField(blank=True)
    children_and_extra_beds_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.hotel.name})"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.hotel.name}-{self.name}")
        super().save(*args, **kwargs)

class RoomImage(models.Model):
    room = models.ForeignKey(Room, related_name="room_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='room_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.room.name}"


class Feature(models.Model):
    room = models.ForeignKey(Room, related_name="features", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    icon = models.ImageField(upload_to='feature_icons/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.room.name}"


class Specification(models.Model):
    room = models.ForeignKey(Room, related_name="specifications", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.ImageField(upload_to='specification_icons/', null=True, blank=True)

    def __str__(self):
        return f"{self.name} - {self.room.name}"
    
# Facility Models
class Facility(models.Model):
    FACILITY_TYPES = [
        ('gym', 'Gym'),
        ('spa', 'Spa'),
        ('clinic', 'Clinic'),
        ('pool', 'Swimming Pool'),
        ('bar', 'Bar / Lounge'),
        ('restaurant', 'Restaurant'),
        ('kids_play_area', "Kids' Play Area"),
        ('game_room', 'Game Room'),
        ('cinema', 'Cinema Room'),
        ('golf', 'Golf Course'),
        ('water_sports', 'Water Sports Center'),
        ('business_center', 'Business Center'),
        ('coworking', 'Co-working Space'),
        ('event_hall', 'Event Hall'),
        ('concierge', 'Concierge'),
        ('shuttle', 'Shuttle Service'),
        ('laundry', 'Laundry Service'),
        ('atm', 'ATM'),
        ('currency_exchange', 'Currency Exchange'),
        ('gift_shop', 'Gift Shop'),
        ('salon', 'Hair / Beauty Salon'),
    ]

    hotel = models.ForeignKey(Hotel, related_name="facilities", on_delete=models.CASCADE)
    type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='facility_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.get_type_display()} - {self.hotel.name}"
    
    class Meta:
        verbose_name_plural = "Facilities"
        