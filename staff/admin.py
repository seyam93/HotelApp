from django.contrib import admin
from .models import Manager

@admin.register(Manager)
class ManagerAdmin(admin.ModelAdmin):
    list_display = ('name', 'hotel', 'position', 'email')
    search_fields = ('name', 'hotel__name', 'email')