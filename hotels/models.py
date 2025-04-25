from django.db import models
from django.template.defaultfilters import slugify
import os
import uuid
from PIL import Image
import io
from django.core.files.base import ContentFile

# Social Media Choices
SOCIAL_CHOICES = [
    ('facebook', 'Facebook'),
    ('instagram', 'Instagram'),
    ('twitter', 'Twitter'),
    ('linkedin', 'LinkedIn'),
    ('youtube', 'YouTube'),
    ('tiktok', 'TikTok'),
    ('tripadvisor', 'TripAdvisor'),
    ('website', 'Official Website'),
    ('whatsapp', 'WhatsApp'),
    ('telegram', 'Telegram'),
    ('sms', 'SMS'),   
    ('pinterest', 'Pinterest'),
    ('snapchat', 'Snapchat'),
    ('reddit', 'Reddit'),
    ('tumblr', 'Tumblr'),
]
# Facility Models
class Facility(models.Model):
    FACILITY_TYPES = [
        ('restaurant', 'Restaurant'),
        ('gym', 'Fitness Center'),
        ('spa', 'Spa'),
        ('clinic', 'Clinic'),
        ('pool', 'Swimming Pool'),
        ('bar', 'Bar / Lounge'),
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

    hotel = models.ForeignKey(
    'hotels.Hotel',
    on_delete=models.CASCADE,
    related_name='facilities',
    null=True,
    blank=True
)
    type = models.CharField(max_length=50, choices=FACILITY_TYPES)
    name = models.CharField(max_length=255)  # Unique *within* hotel
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    notes = models.TextField(blank=True)
    image = models.ImageField(upload_to='facility_images/', null=True, blank=True)
    detail_file = models.FileField(upload_to='facility_files/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Facilities"
        unique_together = ('hotel', 'name')  # 👈 Ensures name is unique per hotel
        ordering = ['type', 'name']

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def clean(self):
        from django.core.exceptions import ValidationError
        if Facility.objects.filter(hotel=self.hotel, name=self.name).exclude(pk=self.pk).exists():
            raise ValidationError(f"A facility with the name '{self.name}' already exists for this hotel.")

    def __str__(self):
        hotel_name = self.hotel.name if self.hotel else "No Hotel"
        return f"{self.name} ({self.get_type_display()}) - {hotel_name}"

# Facility Image Models
class FacilityImage(models.Model):
    facility = models.ForeignKey(
        'Facility',
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='facility_images/')
    caption = models.CharField(max_length=255, blank=True)

    def save(self, *args, **kwargs):

        if self.image:
            img = Image.open(self.image)
            target_width, target_height = 375, 500
            if img.width != target_width or img.height != target_height:
                img = img.resize((target_width, target_height), Image.LANCZOS)
                img_io = io.BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(img_io, format=img_format)
                img_content = ContentFile(img_io.getvalue(), self.image.name)
                self.image.save(self.image.name, img_content, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.facility.name}"
    
# Hotel Models
class Hotel(models.Model):
    name = models.CharField(max_length=255)
    slogan = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255, blank=True)
    star_rating = models.PositiveSmallIntegerField(default=1, choices=[(i, f"{i} Star") for i in range(1, 6)])
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField()
    location = models.CharField(max_length=500, default="")
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    fact_sheet = models.FileField(upload_to='hotel_fact_sheets/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):

        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['name']

class SocialLink(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='social_links', on_delete=models.CASCADE)
    platform = models.CharField(max_length=50, choices=SOCIAL_CHOICES)
    url = models.URLField()

    def __str__(self):
        return f"{self.hotel.name} - {self.get_platform_display()}"

class HotelImage(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="hotel_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='hotel_images/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):

        if self.image:
            img = Image.open(self.image)
            target_width, target_height = 375, 500
            if img.width != target_width or img.height != target_height:
                img = img.resize((target_width, target_height), Image.LANCZOS)
                img_io = io.BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(img_io, format=img_format)
                img_content = ContentFile(img_io.getvalue(), self.image.name)
                self.image.save(self.image.name, img_content, save=False)
        super().save(*args, **kwargs)

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
class Feature(models.Model):
    name = models.CharField(max_length=255, unique=True)
    icon = models.CharField(max_length=200 ,null=True, blank=True )

    def __str__(self):
        return self.name
    
class Room(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="rooms", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    number_of_beds = models.PositiveIntegerField(default=1)
    number_of_bathrooms = models.PositiveIntegerField(default=1)
    area = models.FloatField(help_text="Area in square meters", blank=True)
    includes_breakfast = models.BooleanField(default=True, blank=True)
    room_discount = models.PositiveIntegerField(default=0, blank=True)
    is_suit = models.BooleanField(default=False)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2, blank=True)
    is_available = models.BooleanField(default=True)
    image_cover = models.ImageField(upload_to='room_covers/', null=True, blank=True)
    check_in_notes = models.TextField(blank=True)
    check_out_notes = models.TextField(blank=True)
    special_check_in_instructions = models.TextField(blank=True)
    children_and_extra_beds_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amenities = models.ManyToManyField('Amenity', related_name='amenities', blank=True)
    features = models.ManyToManyField(Feature, related_name='rooms', blank=True)

    def __str__(self):
        return f"{self.name} ({self.hotel.name})"

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

def rename_uploaded_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('room_images', filename)

class RoomImage(models.Model):
    room = models.ForeignKey('Room', related_name="room_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to=rename_uploaded_image)
    caption = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):

        if self.image:
            img = Image.open(self.image)
            target_width, target_height = 1920, 1080
            if img.width != target_width or img.height != target_height:
                img = img.resize((target_width, target_height), Image.LANCZOS)
                img_io = io.BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(img_io, format=img_format)
                img_content = ContentFile(img_io.getvalue(), self.image.name)
                self.image.save(self.image.name, img_content, save=False)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.room.name}"

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=200 ,null=True, blank=True )
    
    def __str__(self):
        return self.name
    
class Specification(models.Model):
    room = models.ForeignKey(Room, related_name="specifications", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    icon = models.CharField(max_length=200 ,null=True, blank=True )

    def __str__(self):
        return f"{self.name} - {self.room.name}"
    
# Review Models
class Review(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='reviews', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    email = models.EmailField(null=True, blank=True)
    profile_picture = models.ImageField(upload_to='review_images/', null=True, blank=True)
    rating = models.PositiveSmallIntegerField(choices=[(i, f"{i} Stars") for i in range(1, 6)])
    comment = models.TextField()
    view_link = models.URLField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)        

# Offer Models
class Offer(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="offers", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    image = models.ImageField(upload_to='offer_images/', null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title
    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        ordering = ['-start_date']

# Service Models ( Breakfast - laundry - etc )
class HotelService(models.Model):
    SERVICE_PERIOD_CHOICES = [
        ('per_night', 'Per Night'),
        ('daily', 'Daily'),
        ('once', 'One Time'),
    ]
    currency_choices = [
        ('USD', 'USD'),
        ('EGP', 'EGP'),  
    ]
    hotel = models.ForeignKey(Hotel, related_name='hotel_services', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    featured = models.BooleanField(default=False)
    image = models.ImageField(upload_to='hotel_services/',help_text="Dimension: 375x500", null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=0,null=True, blank=True)
    pricing_type = models.CharField(max_length=20, choices=SERVICE_PERIOD_CHOICES, default='per_night',null=True, blank=True)
    price_currency = models.CharField(max_length=3, default='EGP',null=True, blank=True, choices=currency_choices)

    def __str__(self):
        return f"{self.title} - {self.hotel.name}"
    
# Image Cover Models
class ImageCover(models.Model):
    hotel = models.ForeignKey('Hotel', related_name='image_covers', on_delete=models.CASCADE, null=True, blank=True)
    room = models.ForeignKey('Room', related_name='image_covers', on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField(upload_to='image_covers/')
    caption = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):

        if self.image:
            img = Image.open(self.image)
            if self.hotel:
                target_width, target_height = 375, 500
            elif self.room:
                target_width, target_height = 1920, 1080
            else:
                target_width, target_height = img.width, img.height  # no resizing if no relation

            if img.width != target_width or img.height != target_height:
                img = img.resize((target_width, target_height), Image.LANCZOS)
                img_io = io.BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(img_io, format=img_format)
                img_content = ContentFile(img_io.getvalue(), self.image.name)
                self.image.save(self.image.name, img_content, save=False)

        super().save(*args, **kwargs)

    def __str__(self):
        if self.hotel:
            return f"Image for Hotel: {self.hotel.name}"
        elif self.room:
            return f"Image for Room: {self.room.name}"
        else:
            return "Unlinked ImageCover"
