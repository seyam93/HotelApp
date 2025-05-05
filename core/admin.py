from django.contrib import admin
from django.utils.html import format_html
from core.models import FAQ, Contact, Newsletter, Feedback, PrivacyPolicy, TermsAndConditions, HotelArticle, ContactMessage, Partner

@admin.register(Partner)
class PartnerAdmin(admin.ModelAdmin):
    list_display = ('partner_name', 'partner_url', 'display_image', 'hotel')
    list_filter = ('hotel',)
    search_fields = ('partner_name', 'partner_description')

    def display_image(self, obj):
        if obj.partner_image:
            return format_html('<img src="{}" width="50" style="border-radius: 4px;" />', obj.partner_image.url)
        return "-"
    display_image.short_description = "Image"

@admin.register(HotelArticle)
class HotelArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'published_date')
    search_fields = ('title', 'content', 'author__username')
    list_filter = ('published_date',)
    prepopulated_fields = {'slug': ('title',)}

@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'hotel', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_filter = ('hotel', 'created_at')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'get_hotels')
    ordering = ('question',)

    def get_hotels(self, obj):
        return ", ".join([h.name for h in obj.hotels.all()])
    get_hotels.short_description = "Hotels"

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'hotel', 'created_at')
    search_fields = ('name', 'email', 'hotel__name')
    list_filter = ('hotel',)
    ordering = ['-created_at']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'get_hotels', 'created_at')
    ordering = ['-created_at']

    def get_hotels(self, obj):
        return ", ".join([h.name for h in obj.hotels.all()])
    get_hotels.short_description = "Hotels"

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'hotel', 'created_at')
    search_fields = ('name', 'email', 'hotel__name')
    list_filter = ('hotel',)
    ordering = ['-created_at']

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_hotels', 'created_at')
    ordering = ['-created_at']

    def get_hotels(self, obj):
        return ", ".join([h.name for h in obj.hotels.all()])
    get_hotels.short_description = "Hotels"

@admin.register(TermsAndConditions)
class TermsAndConditionsAdmin(admin.ModelAdmin):
    list_display = ('title', 'get_hotels', 'created_at')
    ordering = ['-created_at']

    def get_hotels(self, obj):
        return ", ".join([h.name for h in obj.hotels.all()])
    get_hotels.short_description = "Hotels"
