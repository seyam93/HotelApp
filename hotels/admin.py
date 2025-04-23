from django.contrib import admin
from .models import Hotel, HotelImage, WelcomeMessage, Room, RoomImage, Feature, Specification, Facility, Amenity

class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'location', 'created_at')
    search_fields = ('name', 'location')
    inlines = [HotelImageInline, RoomInline]

@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name' )
    
class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

class FeatureInline(admin.TabularInline):
    model = Feature
    extra = 1

class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'hotel', 'price_per_night', 'is_available')
    list_filter = ('is_available', 'is_suit')
    search_fields = ('name', 'hotel__name')
    inlines = [RoomImageInline, FeatureInline, SpecificationInline]

admin.site.register(WelcomeMessage)
admin.site.register(Facility)

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'room')
    search_fields = ('name', 'room__name')
    list_filter = ('room__hotel',)

    