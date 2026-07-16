from rest_framework import serializers
from .models import User, Role

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = ['id', 'name', 'is_system', 'permissions', 'is_active', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    role_name = serializers.CharField(source='role.name', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True, default=None)

    class Meta:
        model = User
        fields = ['id', 'username', 'full_name', 'phone', 'role', 'role_name', 'store', 'store_name', 'is_active']
        extra_kwargs = {'password': {'write_only': True, 'required': False}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        user = super().create(validated_data)
        if password:
            user.set_password(password)
            user.save()
        return user