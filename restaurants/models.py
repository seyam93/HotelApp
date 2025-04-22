from django.db import models
from hotels.models import Hotel  # because Restaurant is linked to Hotel
from django.template.defaultfilters import slugify

# Restaurant Models
class Restaurant(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="restaurants", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True, blank=True, null=True)
    description = models.TextField()
    opening_hours = models.CharField(max_length=100)
    image = models.ImageField(upload_to='restaurant_images/', null=True, blank=True)
    menu_file = models.FileField(upload_to='restaurant_menus/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

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

