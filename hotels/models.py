from django.db import models
from django.template.defaultfilters import slugify
from PIL import Image
import io, os, uuid
from django.core.files.base import ContentFile
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.files.uploadedfile import InMemoryUploadedFile

# Utility function to rename uploaded images
def rename_uploaded_image(instance, filename):
    ext = filename.split('.')[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join('room_images', filename)

# App page background models
class PageBackground(models.Model):
    PAGE_CHOICES = [
        ('hotel_main', 'Hotel Main Page'),
        ('offers', 'Offers Page'),
        ('rooms', 'Rooms Page'),
        ('facilities', 'Facilities Page'),
        ('events', 'Events Page'),
        ('restaurant', 'Restaurant Page'),
        ('spa', 'Spa Page'),
        ('gym', 'Gym Page'),  # Add any other pages you want
    ]

    hotel = models.ForeignKey('hotels.Hotel', on_delete=models.CASCADE, related_name='page_backgrounds')
    page = models.CharField(max_length=50, choices=PAGE_CHOICES)
    image = models.ImageField(upload_to='backgrounds/')
    title = models.CharField(max_length=255, blank=True, null=True)  # Optional: for alt text or SEO
    description = models.TextField(blank=True, null=True)  # Optional: for admins
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.hotel.name} - {self.get_page_display()}"
    
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
    short_note_1 = models.TextField(max_length=200, null=True, blank=True)
    short_note_2 = models.TextField(max_length=200, null=True, blank=True)
    short_note_3 = models.TextField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='facility_images/', null=True, blank=True)
    icon = models.CharField(max_length=200, null=True, blank=True)
    detail_file = models.FileField(upload_to='facility_files/', null=True, blank=True)
    is_featured = models.BooleanField(default=False,help_text="Activating this makes the facility appear in the page")  # to be shown in pages
    slug = models.SlugField(unique=True, blank=True, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Facilities"
        unique_together = ('hotel', 'name')  # 👈 Ensures name is unique per hotel
        ordering = ['type', 'name']

    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Facility.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
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
    image = models.ImageField(upload_to='facility_images/',help_text="Dimension: 375x500 - This Image Will Be Shown Down in The Facility Page")
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
    image_cover = models.ImageField(upload_to='hotel_covers/', null=True, blank=True, help_text="Signature image for carousel and listings")
    star_rating = models.PositiveSmallIntegerField(default=1, choices=[(i, f"{i} Star") for i in range(1, 6)])
    phone = models.CharField(max_length=20, blank=True)
    city = models.CharField(max_length=100, blank=True)
    country = models.CharField(max_length=100, blank=True)
    email = models.EmailField(blank=True)
    address = models.TextField(null=True, blank=True)
    location = models.CharField(max_length=500, default="")
    description = models.TextField()
    slug = models.SlugField(unique=True, blank=True, null=True)
    fact_sheet = models.FileField(upload_to='hotel_fact_sheets/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    contact_banner = models.ImageField(upload_to='contact_banners/', null=True, blank=True,help_text=" For Contact Page")
    contact_image1 = models.ImageField(upload_to='contact_images/', null=True, blank=True,help_text=" For Contact Page")
    contact_image2 = models.ImageField(upload_to='contact_images/', null=True, blank=True,help_text=" For Contact Page")
    map_embed_url = models.CharField(max_length=1500 ,blank=True, null=True,help_text=" For Contact Page")

    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Auto-generate unique slug
        if not self.slug and self.name:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Hotel.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Resize image_cover if provided
        if self.image_cover:
            try:
                img = Image.open(self.image_cover)
                target_width, target_height = 1550, 1080
                if img.width != target_width or img.height != target_height:
                    img = img.resize((target_width, target_height), Image.LANCZOS)
                    img_io = io.BytesIO()
                    img_format = img.format or 'JPEG'
                    img.save(img_io, format=img_format)
                    img_content = ContentFile(img_io.getvalue(), self.image_cover.name)
                    self.image_cover.save(self.image_cover.name, img_content, save=False)
            except Exception as e:
                print(f"Error resizing image_cover: {e}")

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
    BED_TYPES = [
        ('king/twin', 'King / Twin Bed'),
        ('single', 'Single Bed'),
        ('double', 'Double Bed'),
        ('queen', 'Queen Bed'),
        ('king', 'King Bed'),
        ('twin', 'Twin Bed'),
        ('sofa', 'Sofa Bed'),
    ]

    ROOM_VIEWS = [
        ('sea', 'Sea View'),
        ('city', 'City View'),
        ('garden', 'Garden View'),
        ('pool', 'Pool View'),
        ('mountain', 'Mountain View'),
    ]

    hotel = models.ForeignKey('Hotel', related_name="rooms", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    short_description = models.TextField(blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    slug = models.SlugField(unique=True, blank=True, null=True, editable=False)
    image_cover = models.ImageField(upload_to='room_covers/', null=True, blank=True)
    number_of_beds = models.PositiveIntegerField(default=1)
    bed_type = models.CharField(max_length=20, choices=BED_TYPES, default='king/twin')
    room_views = models.CharField(max_length=20, choices=ROOM_VIEWS, default='city')
    number_of_bathrooms = models.PositiveIntegerField(default=1)
    number_of_persons = models.CharField(max_length=50, default="1-2", null=True, blank=True)
    area = models.FloatField(help_text="Area in square meters", blank=True, null=True)
    includes_breakfast = models.BooleanField(default=True, blank=True)
    room_discount = models.PositiveIntegerField(default=0, blank=True)
    is_suit = models.BooleanField(default=False)
    is_available = models.BooleanField(default=True)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=0, blank=True, null=True)
    featured = models.BooleanField(default=False)
    room_features_section_1 = models.TextField(default="Modified_Room Featured Section (Nourhan)",blank=True)
    room_features_section_2 = models.TextField(default="Modified_Room Featured Section 2 (Nourhan)",blank=True)
    room_features_section_3 = models.TextField(default="Modified_Room Featured Section 3 (Nourhan)",blank=True)
    special_check_in_instructions = models.TextField(blank=True)
    children_and_extra_beds_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amenities = models.ManyToManyField('Amenity', related_name='rooms', blank=True)
    features = models.ManyToManyField('Feature', related_name='rooms', blank=True)

    def __str__(self):
        return f"{self.name} ({self.hotel.name})"

    @staticmethod
    def generate_unique_slug(name):
        base_slug = slugify(name)
        unique_id = uuid.uuid4().hex[:8]
        return f"{base_slug}-{unique_id}"

    def get_absolute_url(self):
        return reverse('room-detail', kwargs={'hotel_slug': self.hotel.slug, 'room_slug': self.slug})
    
    def save(self, *args, **kwargs):
        if not self.slug and self.name:
            self.slug = self.generate_unique_slug(self.name)

        # If saving a new image, resize it before saving to DB
        if self.image_cover:
            img = Image.open(self.image_cover)
            target_width, target_height = 1550, 1080
            if img.width != target_width or img.height != target_height:
                img = img.resize((target_width, target_height), Image.LANCZOS)
                img_io = io.BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(img_io, format=img_format)
                img_content = ContentFile(img_io.getvalue(), self.image_cover.name)
                self.image_cover.save(self.image_cover.name, img_content, save=False)

        super().save(*args, **kwargs)
                
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
                img_io.seek(0)
                img_content = ContentFile(img_io.getvalue(), self.image.name)
                self.image.save(self.image.name, img_content, save=False)

        # === Auto-caption ===
        if not self.caption:
            self.caption = f"{self.room.name} Room Image"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"Image for {self.room.name}"

class Amenity(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)
    icon = models.CharField(max_length=200 ,null=True, blank=True )
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name = "Room's Amenity"
        verbose_name_plural = "Room Amenities"
        ordering = ['name']
    
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

    def __str__(self):
        return f"Review by {self.name} for {self.hotel.name}"       

# Offer Models
class Offer(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="offers", on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    terms_and_conditions = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to='offer_images/', null=True, blank=True)
    validity_period = models.CharField(max_length=100, null=True, blank=True)
    offer_code = models.CharField(max_length=50, null=True, blank=True)
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=0, null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    booking_link = models.URLField(null=True, blank=True, help_text="Link to booking page or external site")
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = "Offer"
        verbose_name_plural = "Offers"
        ordering = ['-start_date']

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)

        
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            target_width, target_height = 1920, 1180
            if img.width != target_width or img.height != target_height:
                img = img.resize((target_width, target_height), Image.LANCZOS)

            img_io = io.BytesIO()
            img_format = img.format if img.format else 'JPEG'
            img.save(img_io, format=img_format)
            img_io.seek(0)
            img_content = ContentFile(img_io.getvalue(), self.image.name)
            self.image.save(self.image.name, img_content, save=False)

        super().save(*args, **kwargs)  

# Service Models ( Breakfast - laundry - etc )
class HotelService(models.Model):
    SERVICE_PERIOD_CHOICES = [
        ('Per Night', 'Per Night'),
        ('Daily', 'Daily'),
        ('Once', 'One Time'),
    ]
    currency_choices = [
        ('USD', 'USD'),
        ('EGP', 'EGP'),  
    ]
    hotel = models.ForeignKey(Hotel, related_name='hotel_services', on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.TextField()
    featured = models.BooleanField(default=False, help_text="Activating this makes the service appear in (Pricing Section ) Please no more than 3 services")
    icon = models.CharField(max_length=200, null=True, blank=True)
    image = models.ImageField(upload_to='hotel_services/', help_text="Dimension: 375x500", null=True, blank=True)
    price = models.DecimalField(max_digits=8, decimal_places=0, null=True, blank=True)
    pricing_type = models.CharField(max_length=20, choices=SERVICE_PERIOD_CHOICES, default='Per Night', null=True, blank=True)
    price_currency = models.CharField(max_length=3, default='EGP', null=True, blank=True, choices=currency_choices)
    is_active = models.BooleanField(default=True, help_text="Uncheck to hide this service from frontend")
    
    def __str__(self):
        return f"{self.title} - {self.hotel.name}"

    class Meta:
        verbose_name = "Hotel Service ( Hotel Amenities )"
        verbose_name_plural = "Hotel Services ( Hotel Amenities )"

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
        
# Hotel Banner Models
class HotelPageBanner(models.Model):
    hotel = models.ForeignKey('hotels.Hotel', related_name="banners", on_delete=models.CASCADE)
    page = models.CharField(max_length=100, choices=[
        ('home', 'Home Page'),
        ('rooms', 'Rooms Page'),
        ('restaurants', 'Restaurants Page'),
        ('offers', 'Offers Page'),
        ('spa', 'Spa Page'),
        ('meetings', 'Meetings Page'),
        ('events', 'Events Page'),
        ('gallery', 'Gallery Page'),
        ('contact', 'Contact Page'),
    ])
    image = models.ImageField(upload_to='hotel_banners/')
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hotel', 'page')  # Only one banner per page per hotel
        ordering = ['page']

    def __str__(self):
        return f"{self.hotel.name} - {self.page.capitalize()} Banner"

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            target_width, target_height = 1920, 1080
            if img.width != target_width or img.height != target_height:
                img = img.resize((target_width, target_height), Image.LANCZOS)
                img_io = io.BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(img_io, format=img_format)
                img_io.seek(0)
                img_content = ContentFile(img_io.getvalue(), self.image.name)
                self.image.save(self.image.name, img_content, save=False)
        super().save(*args, **kwargs)

class HotelVideoBanner(models.Model):
    hotel = models.ForeignKey('hotels.Hotel', related_name="video_banners", on_delete=models.CASCADE)
    page = models.CharField(max_length=100, choices=[
        ('home', 'Home Page'),
        ('rooms', 'Rooms Page'),
        ('restaurants', 'Restaurants Page'),
        ('offers', 'Offers Page'),
        ('spa', 'Spa Page'),
        ('meetings', 'Meetings Page'),
        ('events', 'Events Page'),
        ('gallery', 'Gallery Page'),
        ('contact', 'Contact Page'),
    ])
    video_url = models.URLField(blank=True, null=True)
    video_file = models.FileField(upload_to='hotel_video_banners/', blank=True, null=True)
    title = models.CharField(max_length=255, blank=True, null=True)
    subtitle = models.CharField(max_length=255, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('hotel', 'page')  # Only one video banner per page per hotel
        ordering = ['page']

    def __str__(self):
        return f"{self.hotel.name} - {self.page.capitalize()} Video Banner"
    
# Gallery ( Image - Video ) Models
class GalleryItem(models.Model):
    GALLERY_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
    ]

    hotel = models.ForeignKey(Hotel, related_name='gallery_items', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    gallery_type = models.CharField(max_length=10, choices=GALLERY_TYPE_CHOICES, default='image')

    image = models.ImageField(upload_to='gallery/images/', null=True, blank=True)
    video_url = models.URLField(null=True, blank=True)
    video_file = models.FileField(upload_to='gallery/videos/', null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} ({self.gallery_type})"

    def clean(self):
        if self.gallery_type == 'image':
            if not self.image:
                raise ValidationError("Image is required when gallery_type is 'image'.")
            if self.video_url or self.video_file:
                raise ValidationError("Only image should be provided when gallery_type is 'image'.")
        elif self.gallery_type == 'video':
            if not self.video_url and not self.video_file:
                raise ValidationError("Either video_url or video_file is required when gallery_type is 'video'.")
            if self.image:
                raise ValidationError("Image should not be provided when gallery_type is 'video'.")

    def save(self, *args, **kwargs):
        self.full_clean()

        # Delete old image if changed
        if self.pk:
            old = GalleryItem.objects.filter(pk=self.pk).first()
            if old and old.image and self.image != old.image:
                old.image.delete(save=False)

        # Process image
        if self.image:
            try:
                img = Image.open(self.image)
                img = img.convert("RGB")

                target_width, target_height = 1920, 1080
                target_ratio = target_width / target_height
                img_ratio = img.width / img.height

                # Crop to center with same aspect ratio
                if img_ratio > target_ratio:
                    new_width = int(target_ratio * img.height)
                    offset = (img.width - new_width) // 2
                    box = (offset, 0, offset + new_width, img.height)
                else:
                    new_height = int(img.width / target_ratio)
                    offset = (img.height - new_height) // 2
                    box = (0, offset, img.width, offset + new_height)

                img = img.crop(box)
                img = img.resize((target_width, target_height), Image.LANCZOS)

                img_io = io.BytesIO()
                img.save(img_io, format='JPEG', quality=90)
                img_io.seek(0)

                # Generate unique filename
                filename = f"{slugify(self.title)}-{uuid.uuid4().hex}.jpg"
                self.image.save(filename, ContentFile(img_io.getvalue()), save=False)

            except Exception as e:
                raise ValidationError(f"Image processing failed: {e}")

        super().save(*args, **kwargs)

    @property
    def is_image(self):
        return self.gallery_type == 'image' and self.image

    @property
    def is_video_url(self):
        return self.gallery_type == 'video' and self.video_url

    @property
    def is_video_file(self):
        return self.gallery_type == 'video' and self.video_file

    @property
    def youtube_video_id(self):
        if self.video_url and "youtube.com/watch?v=" in self.video_url:
            return self.video_url.split("watch?v=")[-1].split("&")[0]
        elif self.video_url and "youtu.be/" in self.video_url:
            return self.video_url.split("youtu.be/")[-1].split("?")[0]
        return None

    @property
    def youtube_thumbnail_url(self):
        video_id = self.youtube_video_id
        if video_id:
            return f"https://img.youtube.com/vi/{video_id}/hqdefault.jpg"
        return None
    @property
    def embed_video_url(self):
        """Return embed-friendly YouTube URL or fallback to the original."""
        if self.video_url and "youtube.com/watch?v=" in self.video_url:
            video_id = self.video_url.split("watch?v=")[-1].split("&")[0]
            return f"https://youtu.be/{video_id}"
        return self.video_url

    class Meta:
        verbose_name = "Gallery Item"
        verbose_name_plural = "Gallery Items"
        ordering = ['-created_at']

