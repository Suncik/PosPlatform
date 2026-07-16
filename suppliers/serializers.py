from rest_framework import serializers
from .models import Supplier


class SupplierSerializer(serializers.ModelSerializer):
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Supplier
        fields = ['id', 'name', 'contact_person', 'phone', 'address', 'is_active', 'balance', 'created_at']

    def get_balance(self, obj):
     

        return 0