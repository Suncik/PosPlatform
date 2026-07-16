from rest_framework import serializers
from django.db import transaction
from .models import StockTransfer, StockTransferItem
from products.models import Product


class StockTransferItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = StockTransferItem
        fields = ['id', 'product', 'product_name', 'quantity']


class StockTransferSerializer(serializers.ModelSerializer):
    items = StockTransferItemSerializer(many=True)
    source_store_name = serializers.CharField(source='source_store.name', read_only=True)
    destination_store_name = serializers.CharField(source='destination_store.name', read_only=True)
    total_amount = serializers.SerializerMethodField()

    class Meta:
        model = StockTransfer
        fields = [
            'id', 'number', 'source_store', 'source_store_name',
            'destination_store', 'destination_store_name',
            'comment', 'status', 'items', 'total_amount', 'created_at'
        ]

    def get_total_amount(self, obj):
        return float(sum(float(i.quantity) * float(i.product.cost_price) for i in obj.items.all()))

    def validate(self, data):
        if data.get('source_store') == data.get('destination_store'):
            raise serializers.ValidationError({"error": "Manba va maqsad filial bir xil bo'lishi mumkin emas!"})
        if not data.get('items'):
            raise serializers.ValidationError({"error": "Kamida bitta mahsulot qo'shing"})
        return data

    def create(self, validated_data):
        items_data = validated_data.pop('items')

        with transaction.atomic():
            transfer = StockTransfer.objects.create(**validated_data)
            destination_store = transfer.destination_store

            for item_data in items_data:
                source_product = item_data['product']
                quantity = item_data['quantity']

                if source_product.stock < quantity:
                    raise serializers.ValidationError(
                        {"error": f"{source_product.name} mahsulotidan omborda yetarli emas! Qoldiq: {source_product.stock}"}
                    )

                StockTransferItem.objects.create(transfer=transfer, product=source_product, quantity=quantity)

                # Manba filialdan kamaytiramiz
                source_product.stock -= quantity
                source_product.save()

                
                dest_product = None
                if source_product.barcode:
                    dest_product = Product.objects.filter(store=destination_store, barcode=source_product.barcode).first()
                if not dest_product:
                    dest_product = Product.objects.filter(store=destination_store, name=source_product.name).first()

                if dest_product:
                    dest_product.stock += quantity
                    dest_product.save()
                else:
                    # Maqsad filialda bunday mahsulot umuman yo'q — avtomatik yaratamiz
                    Product.objects.create(
                        category=source_product.category,
                        name=source_product.name,
                        barcode=source_product.barcode,
                        plu=source_product.plu,
                        unit=source_product.unit,
                        cost_price=source_product.cost_price,
                        selling_price=source_product.selling_price,
                        stock=quantity,
                        store=destination_store,
                    )

            return transfer