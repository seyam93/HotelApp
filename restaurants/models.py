from django.db import models
from hotels.models import Hotel  # because Restaurant is linked to Hotel
from django.template.defaultfilters import slugify
from django.core.files.base import ContentFile
from PIL import Image
import io
from django.urls import reverse
from django.utils.html import mark_safe
from django.conf import settings
from utils.qr_code_generator import generate_qr_code 

# Restaurant Models
class Restaurant(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="restaurants", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    slogan = models.CharField(max_length=255, null=True, blank=True,default="Address Of Taste")
    display_order = models.PositiveIntegerField(default=0, null=True, blank=True)
    description = models.TextField()
    short_description = models.TextField(null=True, blank=True)
    no_of_seats = models.PositiveIntegerField(default=0, null=True, blank=True)
    opening_hours = models.CharField(max_length=100,null=True, blank=True)
    breakfast_hours = models.CharField(max_length=100, null=True, blank=True,default="Breakfast: 6.00 am – 11.00 am (daily)")
    lunch_hours = models.CharField(max_length=100,null=True, blank=True,default="Lunch: 12.00 pm – 3.00 pm (daily)")
    dinner_hours = models.CharField(max_length=100,null=True, blank=True,default="Dinner: 6.00 pm – 11.00 pm (daily)")
    dress_code = models.CharField(max_length=100, null=True, blank=True)
    cuisine = models.CharField(max_length=100, null=True, blank=True)
    terrace = models.BooleanField(default=False,null=True, blank=True)
    image_cover = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    menu_file = models.FileField(upload_to='restaurant_menus/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['display_order']

    def save(self, *args, **kwargs):
        if self.image_cover:
            img = Image.open(self.image_cover.file)
            target_width, target_height = 1920, 1080
            if img.width != target_width or img.height != target_height:
                img = img.resize((target_width, target_height), Image.LANCZOS)
                img_io = io.BytesIO()
                img_format = img.format if img.format else 'JPEG'
                img.save(img_io, format=img_format)
                img_io.seek(0)
                img_content = ContentFile(img_io.getvalue(), self.image_cover.name)
                self.image_cover.save(self.image_cover.name, img_content, save=False)

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('restaurant-detail', kwargs={
            'hotel_slug': self.hotel.slug,
            'slug': self.slug
        })

# Restaurant Menus Model  
class RestaurantMenu(models.Model):
    restaurant = models.OneToOneField('Restaurant', on_delete=models.CASCADE, related_name='menu')
    slug = models.SlugField(unique=True, blank=True)

    general_pdf = models.FileField(upload_to='menus/general/', blank=True, null=True)
    breakfast_pdf = models.FileField(upload_to='menus/breakfast/', blank=True, null=True)
    lunch_pdf = models.FileField(upload_to='menus/lunch/', blank=True, null=True)
    dinner_pdf = models.FileField(upload_to='menus/dinner/', blank=True, null=True)
    beverage_pdf = models.FileField(upload_to='menus/beverage/', blank=True, null=True)
    offers_pdf = models.FileField(upload_to='menus/offers/', blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.restaurant.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('restaurant-menu', kwargs={'slug': self.slug})

    def qr_code_preview(self):
        full_url = f"{settings.SITE_DOMAIN}{self.get_absolute_url()}"
        qr_data_uri = generate_qr_code(full_url)
        return mark_safe(f'<img src="{qr_data_uri}" width="150" height="150" />')

    qr_code_preview.short_description = "QR Code"

    def __str__(self):
        return f"{self.restaurant.name} Menus"

  
class RestaurantImage(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="gallery_images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='restaurant_gallery/', null=True, blank=True)
    caption = models.CharField(max_length=255, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image.file)
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

    def __str__(self):
        return f"Image for {self.restaurant.name}"

class MenuCategory(models.Model):
    restaurant = models.ForeignKey(Restaurant, related_name="menu_categories", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.restaurant.name}"

    
class MenuItem(models.Model):
    category = models.ForeignKey(MenuCategory, related_name="menu_items", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    image = models.ImageField(upload_to='menu_item_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.category.name}"

