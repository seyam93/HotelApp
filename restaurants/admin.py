from django.contrib import admin
from .models import Restaurant, MenuCategory, MenuItem, RestaurantImage

class RestaurantImageInline(admin.TabularInline):
    model = RestaurantImage
    extra = 1

@admin.register(Restaurant)
class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'opening_hours')
    search_fields = ('name', 'hotel__name')
    inlines = [RestaurantImageInline]  # ✅ Move inline here!

@admin.register(MenuCategory)
class MenuCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'restaurant', 'created_at')
    search_fields = ('name', 'restaurant__name')

@admin.register(MenuItem)
class MenuItemAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'price', 'created_at')
    search_fields = ('name', 'category__name')
    list_filter = ('category__restaurant',)

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

