from rest_framework import serializers
from django.db import transaction
from .models import StockReceipt, StockReceiptItem
from products.models import Product


class StockReceiptItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = StockReceiptItem
        fields = ['id', 'product', 'product_name', 'quantity', 'cost_price', 'batch_number', 'expiry_date', 'line_total']


class StockReceiptSerializer(serializers.ModelSerializer):
    items = StockReceiptItemSerializer(many=True)
    supplier_name = serializers.CharField(source='supplier.name', read_only=True, default="—")
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = StockReceipt
        fields = ['id', 'number', 'supplier', 'supplier_name', 'store', 'comment', 'items', 'total_amount', 'created_at']
        read_only_fields = ['store']  
    def get_total_amount(self, obj):
        return float(sum(item.line_total for item in obj.items.all()))

    def create(self, validated_data):
        items_data = validated_data.pop('items')
        if not items_data:
            raise serializers.ValidationError({"error": "Tovar qo'shing"})

        with transaction.atomic():
            receipt = StockReceipt.objects.create(**validated_data)

            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                new_cost = item_data['cost_price']

                StockReceiptItem.objects.create(receipt=receipt, **item_data)

                old_stock = product.stock
                old_cost = product.cost_price
                total_qty = old_stock + quantity

                if total_qty > 0:
                    product.cost_price = ((old_stock * old_cost) + (quantity * new_cost)) / total_qty
                product.stock = total_qty
                product.save()

            return receipt