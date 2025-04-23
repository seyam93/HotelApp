from django.contrib import admin
from core.models import FAQ, Contact, Newsletter, Feedback, PrivacyPolicy, TermsAndConditions

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