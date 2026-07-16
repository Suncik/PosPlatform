from django.contrib import admin
from .models import Store, SystemSettings

@admin.register(Store)
class StoreAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']

@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):
    list_display = ['id']