from django.db import models
from hotels.models import Hotel  # because Manager is linked to Hotel
from PIL import Image
import io
from django.core.files.base import ContentFile

class Manager(models.Model):
    hotel = models.ForeignKey(Hotel, related_name='managers', on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    facebook = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    linkedin = models.URLField(blank=True, null=True)
    position = models.CharField(max_length=100)
    image = models.ImageField(upload_to='manager_images/', null=True, blank=True)
    cv = models.FileField(upload_to='manager_cvs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.hotel.name}"

    class Meta:
        ordering = ['name']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.image:
            from PIL import Image
            img = Image.open(self.image.path)
            target_size = (800, 800)
            if img.size != target_size:
                img = img.resize(target_size, Image.LANCZOS)
                img.save(self.image.path)