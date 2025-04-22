from django.db import models
from hotels.models import Hotel  # linked via ForeignKey

class MeetingRoom(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="meeting_rooms", on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    capacity = models.PositiveIntegerField(null=True, blank=True, help_text="Maximum number of people the room can accommodate.")
    area = models.FloatField(default=30 ,help_text="Area in square meters")
    description = models.TextField()
    image = models.ImageField(upload_to='meeting_room_images/', null=True, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.hotel.name} (Capacity: {self.capacity}, Area: {self.area} m²)"