from django.db import models
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status
from .models import Category, Product
from .serializers import CategorySerializer, ProductSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('-created_at')
    serializer_class = CategorySerializer


class ProductViewSet(viewsets.ModelViewSet):
    serializer_class = ProductSerializer

    def get_queryset(self):
        queryset = Product.objects.all().order_by('-created_at')
        params = self.request.query_params

        search = params.get('search')
        category_id = params.get('category')
        store_id = params.get('store')
        unit = params.get('unit')
        stock_op = params.get('stock_op')
        stock_val = params.get('stock_val')

        if search:
            queryset = queryset.filter(models.Q(name__icontains=search) | models.Q(barcode__icontains=search))
        if category_id:
            queryset = queryset.filter(category_id=category_id)
        if store_id:
            queryset = queryset.filter(store_id=store_id)
        if unit:
            queryset = queryset.filter(unit=unit)
        if stock_op and stock_val:
            try:
                val = float(stock_val)
                if stock_op == '=':
                    queryset = queryset.filter(stock=val)
                elif stock_op == '>':
                    queryset = queryset.filter(stock__gt=val)
                elif stock_op == '<':
                    queryset = queryset.filter(stock__lt=val)
                elif stock_op == '>=':
                    queryset = queryset.filter(stock__gte=val)
                elif stock_op == '<=':
                    queryset = queryset.filter(stock__lte=val)
            except ValueError:
                pass
        return queryset

    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', None)
        store_id = request.query_params.get('store_id', None)

        if not query:
            return Response({"error": "Qidiruv matni kiritilmadi"}, status=status.HTTP_400_BAD_REQUEST)

        products = Product.objects.filter(is_active=True)
        if store_id:
            products = products.filter(store_id=store_id)

        products = products.filter(models.Q(name__icontains=query) | models.Q(barcode=query))
        serializer = self.get_serializer(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)