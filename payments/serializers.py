from rest_framework import serializers
from .models import Kassa


class KassaSerializer(serializers.ModelSerializer):
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = Kassa
        fields = ['id', 'store', 'store_name', 'name', 'balance', 'is_active', 'created_at']