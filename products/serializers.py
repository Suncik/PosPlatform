from rest_framework import serializers
from .models import Category, Product

class CategorySerializer(serializers.ModelSerializer):
    products_count = serializers.IntegerField(source='products.count', read_only=True)

    class Meta:
        model = Category
        fields = ['id', 'name', 'description', 'is_active', 'products_count', 'created_at']


class ProductSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    store_name = serializers.CharField(source='store.name', read_only=True, default=None)
    markup_percent = serializers.SerializerMethodField()

    class Meta:
        model = Product
        fields = [
            'id', 'category', 'category_name', 'name', 'barcode', 'plu',
            'description', 'unit', 'has_vat', 'has_marking', 'supplier_name',
            'cost_price', 'selling_price', 'stock', 'is_weighted',
            'store', 'store_name', 'is_active', 'created_at', 'markup_percent',
        ]

    def get_markup_percent(self, obj):
        if obj.cost_price and obj.cost_price > 0:
            return round(float((obj.selling_price - obj.cost_price) / obj.cost_price * 100), 1)
        return 0