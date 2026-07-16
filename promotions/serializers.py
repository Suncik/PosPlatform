from rest_framework import serializers
from .models import Promotion


class PromotionSerializer(serializers.ModelSerializer):
    category_name = serializers.CharField(source='category.name', read_only=True, default=None)
    product_name = serializers.CharField(source='product.name', read_only=True, default=None)
    status = serializers.CharField(read_only=True)

    class Meta:
        model = Promotion
        fields = [
            'id', 'name', 'discount_percent', 'scope', 'category', 'category_name',
            'product', 'product_name', 'start_date', 'end_date', 'is_active', 'status', 'created_at'
        ]

    def validate(self, data):
        scope = data.get('scope', getattr(self.instance, 'scope', 'ALL'))
        if scope == 'CATEGORY' and not data.get('category'):
            raise serializers.ValidationError({"category": "Kategoriya bo'yicha aksiya uchun kategoriyani tanlang"})
        if scope == 'PRODUCT' and not data.get('product'):
            raise serializers.ValidationError({"product": "Bitta mahsulot uchun mahsulotni tanlang"})
        return data