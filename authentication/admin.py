

from django.contrib import admin
from .models import User, Role  # O'zingizning User va Role modellaringiz

# Custom User modelini admin panelga qo'shamiz
@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    # Admin panel ro'yxatida qaysi ustunlar ko'rinishini belgilaymiz
    list_display = ('username', 'phone', 'is_superuser', 'is_staff')
    # Qidiruv berish uchun ustunlar
    search_fields = ('username', 'phone')

# Agar kerak bo'lsa, Role modelini ham qo'shib qo'yamiz
@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ('id', 'name') if hasattr(Role, 'name') else ('id',)