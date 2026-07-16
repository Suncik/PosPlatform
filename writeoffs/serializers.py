from rest_framework import serializers
from .models import WriteOff, WriteOffItem


class WriteOffItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    total_cost = serializers.SerializerMethodField()

    class Meta:
        model = WriteOffItem
        fields = ['id', 'product', 'product_name', 'quantity', 'cost_price', 'total_cost']

    def get_total_cost(self, obj):
        return float(obj.quantity * obj.cost_price)


class WriteOffSerializer(serializers.ModelSerializer):
    items = WriteOffItemSerializer(many=True, read_only=True)
    total_cost = serializers.SerializerMethodField()
    created_by_name = serializers.CharField(source='created_by.full_name', read_only=True, default='—')

    class Meta:
        model = WriteOff
        fields = ['id', 'reason', 'store', 'created_by', 'created_by_name', 'created_at', 'items', 'total_cost']

    def get_total_cost(self, obj):
        return float(sum(item.quantity * item.cost_price for item in obj.items.all()))