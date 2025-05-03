from django.db import models
from hotels.models import Hotel
from meeting_rooms.models import MeetingRoom

class Event(models.Model):
    hotel = models.ForeignKey(Hotel, related_name="events", on_delete=models.CASCADE)
    meeting_room = models.ForeignKey(
        MeetingRoom,
        related_name="events",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Select the room where the event will take place."
    )
    name = models.CharField(max_length=255)
    image = models.ImageField(upload_to='event_images/', null=True, blank=True)
    description = models.TextField()
    short_description = models.TextField(null=True, blank=True)
    venue = models.CharField(max_length=255, blank=True)  # Optional free-text venue if not a room
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name