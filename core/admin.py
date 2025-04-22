from django.contrib import admin
from .models import FAQ, Contact, Newsletter, Feedback, PrivacyPolicy

# Register your models here.
@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'hotel')
    search_fields = ('question', 'hotel__name')
    list_filter = ('hotel',)
    ordering = ['-hotel']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'hotel', 'created_at')
    search_fields = ('name', 'email', 'hotel__name')
    list_filter = ('hotel',)
    ordering = ['-created_at']

@admin.register(Newsletter)
class NewsletterAdmin(admin.ModelAdmin):
    list_display = ('email', 'hotel', 'created_at')
    search_fields = ('email', 'hotel__name')
    list_filter = ('hotel',)
    ordering = ['-created_at']

@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'hotel', 'created_at')
    search_fields = ('name', 'email', 'hotel__name')
    list_filter = ('hotel',)
    ordering = ['-created_at']

@admin.register(PrivacyPolicy)
class PrivacyPolicyAdmin(admin.ModelAdmin):
    list_display = ('title', 'hotel', 'created_at')
    search_fields = ('title', 'hotel__name')
    list_filter = ('hotel',)
    ordering = ['-created_at']

