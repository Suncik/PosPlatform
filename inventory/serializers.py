from rest_framework import serializers
from .models import Inventory, InventoryItem


class InventoryItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)
    barcode = serializers.CharField(source='product.barcode', read_only=True, default=None)
    difference = serializers.SerializerMethodField()

    class Meta:
        model = InventoryItem
        fields = ['id', 'product', 'product_name', 'barcode', 'expected_qty', 'actual_qty', 'difference']

    def get_difference(self, obj):
        return float(obj.actual_qty - obj.expected_qty)


class InventorySerializer(serializers.ModelSerializer):
    items = InventoryItemSerializer(many=True, read_only=True)
    items_count = serializers.SerializerMethodField()

    class Meta:
        model = Inventory
        fields = ['id', 'number', 'store', 'status', 'created_at', 'applied_at', 'items', 'items_count']

    def get_items_count(self, obj):
        return obj.items.count()