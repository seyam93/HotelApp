from django.contrib import admin
from .models import MeetingRoom

@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'capacity', 'available')
    list_filter = ('available',)
    search_fields = ('name', 'hotel__name')