from django.contrib import admin
from .models import Hotel, HotelImage, WelcomeMessage, Room, RoomImage, Feature, Specification, Facility, Amenity, Offer, Review, HotelService

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


class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id','name', 'hotel', 'price_per_night', 'is_available')
    list_filter = ('is_available', 'is_suit')
    search_fields = ('name', 'hotel__name')
    inlines = [RoomImageInline, SpecificationInline]

admin.site.register(WelcomeMessage)
admin.site.register(Facility)

@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)  
    search_fields = ('name',)

@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'room')
    search_fields = ('name', 'room__name')
    list_filter = ('room',)

@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'hotel', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('title', 'hotel__name')
    list_filter = ('hotel', 'start_date', 'end_date')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'name', 'rating', 'created_at')
    search_fields = ('hotel__name', 'name')
    list_filter = ('hotel', 'rating', 'created_at')

@admin.register(HotelService)
class HotelServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'hotel', 'pricing_type', 'price')
    list_filter = ('hotel', 'pricing_type')
    search_fields = ('title', 'description')

 