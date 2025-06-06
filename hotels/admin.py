from django.utils.html import format_html
from django.contrib import admin
from .models import (
    Hotel, HotelImage, WelcomeMessage, Room, RoomImage,
    Feature, Specification, Facility, Amenity, Offer,
    Review, FacilityImage, SocialLink, ImageCover, HotelService,
    PageBackground, HotelPageBanner, HotelVideoBanner, GalleryItem,
    NewsletterSubscriber, HoverSection, HoverImageTab
)
from adminsortable2.admin import SortableTabularInline
from adminsortable2.admin import SortableAdminBase

# ========== Inlines ==========
class HotelImageInline(admin.TabularInline):
    model = HotelImage
    extra = 1

class ImageCoverInline(admin.TabularInline):
    model = ImageCover
    extra = 1

class RoomInline(SortableTabularInline):
    model = Room
    extra = 0
    can_delete = True
    fields = ('name', 'display_order', 'is_available')
    readonly_fields = ('display_order',)

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

class HoverImageTabInline(admin.TabularInline):
    model = HoverImageTab
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
class HotelAdmin(SortableAdminBase, admin.ModelAdmin):
    list_display = ('id', 'name', 'location', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('location',)
    readonly_fields = ('slug', 'created_at', 'updated_at')
    inlines = [HotelImageInline, ImageCoverInline, RoomInline, SocialLinkInline]

    fields = [f.name for f in Hotel._meta.fields if f.editable and f.name not in ('id',)]

# ========== Room (basic admin, no ordering here) ==========
@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('display_order', 'id', 'name', 'hotel', 'price_per_night', 'is_available')
    list_filter = ('is_available', 'is_suit', 'hotel')
    search_fields = ('name', 'hotel__name')
    readonly_fields = ('slug',)

# ========== Amenity ==========
@admin.register(Amenity)
class AmenityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

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

# ========== Hotel Service ==========
@admin.register(HotelService)
class HotelServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'hotel', 'pricing_type', 'price')
    search_fields = ('title', 'description')
    list_filter = ('hotel', 'pricing_type')

# ========== WelcomeMessage ==========
admin.site.register(WelcomeMessage)

# ========== Page Background ==========
@admin.register(PageBackground)
class PageBackgroundAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'page', 'image', 'created_at')
    list_filter = ('page', 'hotel')
    search_fields = ('hotel__name', 'page')

# ========== Hotel Page Banner ==========
@admin.register(HotelPageBanner)
class HotelPageBannerAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'page', 'banner_preview', 'created_at')
    list_filter = ('hotel', 'page')
    search_fields = ('hotel__name', 'page')

    def banner_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" />', obj.image.url)
        return "-"
    banner_preview.short_description = 'Banner Preview'

# ========== Hotel Video Banner ==========
@admin.register(HotelVideoBanner)
class HotelVideoBannerAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'page', 'video_link', 'created_at')
    list_filter = ('hotel', 'page')
    search_fields = ('hotel__name', 'page')

    def video_link(self, obj):
        if obj.video_url:
            return format_html('<a href="{}" target="_blank">View Video</a>', obj.video_url)
        return "-"
    video_link.short_description = 'Video URL'

# ========== Gallery Item ==========
@admin.register(GalleryItem)
class GalleryItemAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'image_preview')
    list_filter = ('hotel',)
    search_fields = ('hotel__name',)

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="200" />', obj.image.url)
        return "-"
    image_preview.short_description = 'Image Preview'

# ========== SocialLink ==========
@admin.register(SocialLink)
class SocialLinkAdmin(admin.ModelAdmin):
    list_display = ('hotel', 'platform', 'url')
    list_filter = ('hotel', 'platform')
    search_fields = ('hotel__name', 'platform')

# ========== Newsletter Subscriber ==========
@admin.register(NewsletterSubscriber)
class NewsletterSubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at') 
    search_fields = ('email',)
    list_filter = ('subscribed_at',)

# ========== Hover Section ==========
@admin.register(HoverSection)
class HoverSectionAdmin(admin.ModelAdmin):
    inlines = [HoverImageTabInline]