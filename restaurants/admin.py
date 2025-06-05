from django.contrib import admin
from adminsortable2.admin import SortableTabularInline
from .models import Restaurant, MenuCategory, MenuItem, RestaurantImage, RestaurantMenu
from django.utils.html import format_html
from utils.qr_code_generator import generate_qr_code 
from django.conf import settings

# ========== Inline for Restaurant (used in HotelAdmin) ==========
class RestaurantInline(SortableTabularInline):
    model = Restaurant
    extra = 1
    fields = ('name', 'display_order', 'slogan', 'no_of_seats')
    readonly_fields = ('display_order',)

# ========== Inline for RestaurantImage ==========
class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1

# ========== Admin for Restaurant ==========
@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('display_order', 'name', 'hotel', 'opening_hours')
    search_fields = ('name', 'hotel__name')
    list_filter = ('hotel',)
    readonly_fields = ('slug',)
    inlines = [RestaurantImageInline]

# ========== Admin for RestaurantMenu ==========
@admin.register(RestaurantMenu)
class RestaurantMenuAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'last_updated', 'qr_code_display')
    readonly_fields = ('slug', 'qr_code_display')

    def qr_code_display(self, obj):
        if not obj.slug:
            return "Save to generate QR"
        url = f"{settings.SITE_DOMAIN}{obj.get_absolute_url()}"
        qr = generate_qr_code(url)
        return format_html('<img src="{}" width="150" height="150" />', qr)

    qr_code_display.short_description = "QR Code"

# ========== Admin for MenuCategory ==========
@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'created_at')
    search_fields = ('name', 'restaurant__name')
    list_filter = ('restaurant',)

# ========== Admin for MenuItem ==========
@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category__restaurant',)

# ========== Admin for RestaurantImage ==========
@admin.register(RestaurantImage)
class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'image')
    search_fields = ('restaurant__name',)
    list_filter = ('restaurant',)
    fieldsets = (
        (None, {
            'fields': ('restaurant', 'image', 'caption')
        }),
    )