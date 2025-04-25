from django.contrib import admin
from .models import (
    Hotel, HotelImage, WelcomeMessage, Room, RoomImage,
    Feature, Specification, Facility, Amenity, Offer,
    Review, FacilityImage, SocialLink, ImageCover, HotelService
)

# ========== Inlines ==========
class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1

class ImageCoverInline(admin.TabularInline):
    model = ImageCover
    extra = 1

class RoomInline(admin.TabularInline):
    model = Room
    extra = 1

class RoomImageInline(admin.TabularInline):
    model = RoomImage
    extra = 1

class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 1

class FacilityImageInline(admin.TabularInline):
    model = FacilityImage
    extra = 1

class SocialLinkInline(admin.TabularInline):
    model = SocialLink
    extra = 1
# ========== Facility ==========
@admin.register(FacilityImage)
class FacilityImageAdmin(admin.ModelAdmin):
    list_display = ('id', 'facility', 'image')
    search_fields = ('facility__name',)
    list_filter = ('facility',)

@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hotel', 'type', 'is_active')
    search_fields = ('name', 'hotel__name')
    list_filter = ('hotel', 'type', 'is_active')
    inlines = [FacilityImageInline]

# ========== Hotel ==========
@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('location',)
    inlines = [HotelImageInline, ImageCoverInline, RoomInline, SocialLinkInline]


# ========== Amenity ==========
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

# ========== Room ==========
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'hotel', 'price_per_night', 'is_available')
    list_filter = ('is_available', 'is_suit', 'hotel')
    search_fields = ('name', 'hotel__name')
    inlines = [ImageCoverInline, RoomImageInline, SpecificationInline]

# ========== Feature ==========
@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

# ========== Specification ==========
@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    list_display = ('name', 'room')
    search_fields = ('name', 'room__name')
    list_filter = ('room',)

# ========== Offer ==========
@admin.register(Offer)
class OfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'hotel', 'discount_percentage', 'start_date', 'end_date')
    search_fields = ('title', 'hotel__name')
    list_filter = ('hotel', 'start_date', 'end_date')

# ========== Review ==========
@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'name', 'rating', 'created_at')
    search_fields = ('hotel__name', 'name')
    list_filter = ('hotel', 'rating', 'created_at')

#========== Hotel Service ==========

@admin.register(HotelService)
class HotelServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'hotel', 'pricing_type', 'price')
    search_fields = ('title', 'description')
    list_filter = ('hotel', 'pricing_type')

# ========== WelcomeMessage ==========
admin.site.register(WelcomeMessage)


