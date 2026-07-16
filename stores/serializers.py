from rest_framework import serializers
from .models import Store, SystemSettings

class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Store
        fields = '__all__'
    
    def get_staff(self, obj):
        return [
            {
                'id': u.id,
                'full_name': u.full_name,
                'role_name': u.role.name if u.role else '—',
                'is_active': u.is_active,
            }
            for u in obj.staff.all()
        ]

    def get_staff_count(self, obj):
        return obj.staff.count()

class SystemSettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemSettings
        fields = '__all__'
        
