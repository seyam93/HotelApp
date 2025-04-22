from django.db import models
from hotels.models import Hotel  # because Manager is linked to Hotel

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