from rest_framework import serializers
from .models import Sale, SaleItem
from products.models import Product
# sales/serializers.py ichiga qo'shing:
from .models import Shift

from django.db.models import Sum

class ShiftSerializer(serializers.ModelSerializer):
    cashier_name = serializers.CharField(source='cashier.full_name', read_only=True)
    sotuv_jami = serializers.SerializerMethodField()
    farq = serializers.SerializerMethodField()

    class Meta:
        model = Shift
        fields = '__all__'

    def get_sotuv_jami(self, obj):
        total = Sale.objects.filter(shift=obj).aggregate(total=Sum('total_amount'))['total'] or 0
        return float(total)

    def get_farq(self, obj):
        if obj.is_open:
            return None
        naqd_sof = Sale.objects.filter(shift=obj).aggregate(total=Sum('paid_cash'))['total'] or 0
        kutilgan = float(obj.opening_balance or 0) + float(naqd_sof)
        sanalgan = float(obj.closing_balance or 0)
        return sanalgan - kutilgan

class SaleItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source='product.name', read_only=True)

    class Meta:
        model = SaleItem
        fields = ['id', 'product', 'product_name', 'quantity', 'price', 'total_price']


class SaleSerializer(serializers.ModelSerializer):
    items = SaleItemSerializer(many=True) 
    cashier_name = serializers.CharField(source='cashier.full_name', read_only=True)
    store_name = serializers.CharField(source='store.name', read_only=True)

    class Meta:
        model = Sale
        fields = [
            'id', 'store', 'store_name', 'cashier', 'cashier_name', 
            'total_amount', 'paid_cash', 'paid_card', 'payment_method', 
            'items', 'created_at'
        ]


    def create(self, validated_data):
        from django.db import transaction
        
        items_data = validated_data.pop('items')
        
   
        with transaction.atomic():
           
            sale = Sale.objects.create(**validated_data)
            
     
            for item_data in items_data:
                product = item_data['product']
                quantity = item_data['quantity']
                
              
                if product.stock < quantity:
                    raise serializers.ValidationError(
                        {"error": f"{product.name} mahsulotidan omborda yetarli emas! Qoldiq: {product.stock}"}
                    )
                
               
                product.stock -= quantity
                product.save()
                
               
                SaleItem.objects.create(sale=sale, **item_data)
                
            return sale