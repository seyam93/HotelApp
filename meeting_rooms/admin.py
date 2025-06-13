from django.contrib import admin
from django.utils.html import format_html
from .models import MeetingRoom, MeetingRoomAmenity, SeatingArrangement, MeetingRoomImages, EventBrochure

class MeetingRoomImageInline(admin.TabularInline):
    model = MeetingRoomImages
    extra = 1
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

@admin.register(MeetingRoom)
class MeetingRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'capacity', 'available', 'area')
    list_filter = ('available', 'hotel', 'amenities', 'seating_arrangements')
    search_fields = ('name', 'hotel__name')
    filter_horizontal = ('amenities', 'seating_arrangements')
    inlines = [MeetingRoomImageInline]

    def list_amenities(self, obj):
        return ", ".join(a.name for a in obj.amenities.all())
    list_amenities.short_description = 'Amenities'

    def list_seating(self, obj):
        return ", ".join(s.name for s in obj.seating_arrangements.all())
    list_seating.short_description = 'Seating Types'

@admin.register(MeetingRoomAmenity)
class MeetingRoomAmenityAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon')
    search_fields = ('name',)

@admin.register(SeatingArrangement)
class SeatingArrangementAdmin(admin.ModelAdmin):
    list_display = ('name', 'capacity', 'image_preview')
    search_fields = ('name',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

@admin.register(MeetingRoomImages)
class MeetingRoomImagesAdmin(admin.ModelAdmin):
    list_display = ('meeting_room', 'created_at', 'image_preview')
    search_fields = ('meeting_room__name',)
    list_filter = ('created_at',)
    readonly_fields = ('image_preview',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="height: 100px;" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Preview'

@admin.register(EventBrochure)
class EventBrochureAdmin(admin.ModelAdmin):
    list_display = ('title', 'qr_code_preview')
    readonly_fields = ('qr_code_preview',)
