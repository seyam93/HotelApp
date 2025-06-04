from django.contrib import admin
from adminsortable2.admin import SortableTabularInline
from .models import Restaurant, MenuCategory, MenuItem, RestaurantImage

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