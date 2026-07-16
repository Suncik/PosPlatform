import datetime
from datetime import date
from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from products.models import Product
from .models import Inventory, InventoryItem
from .serializers import InventorySerializer


class InventoryViewSet(viewsets.ModelViewSet):
    serializer_class = InventorySerializer

    def get_queryset(self):
        user = self.request.user
        qs = Inventory.objects.all().order_by('-created_at')
        if user.is_authenticated and user.role and user.role.name != "Admin":
            qs = qs.filter(store=user.store)
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        user = request.user
        store = user.store if user.is_authenticated else None

        today_str = date.today().strftime('%Y%m%d')
        today_count = Inventory.objects.filter(number__startswith=f'INV-{today_str}').count() + 1
        number = f'INV-{today_str}-{today_count:04d}'

        inventory = Inventory.objects.create(
            number=number,
            store=store,
            created_by=user if user.is_authenticated else None,
        )

        products_qs = Product.objects.filter(is_active=True)
        if store:
            products_qs = products_qs.filter(store=store)

        for product in products_qs:
            InventoryItem.objects.create(
                inventory=inventory,
                product=product,
                expected_qty=product.stock,
                actual_qty=0,
            )

        serializer = self.get_serializer(inventory)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def save_counts(self, request, pk=None):
        """Haqiqiy miqdorlarni saqlash: POST /api/inventory/list/{id}/save_counts/"""
        inventory = self.get_object()
        if inventory.status != 'draft':
            return Response({"error": "Bu inventarizatsiya allaqachon tasdiqlangan!"}, status=status.HTTP_400_BAD_REQUEST)

        for item_data in request.data.get('items', []):
            try:
                item = InventoryItem.objects.get(id=item_data['item_id'], inventory=inventory)
                item.actual_qty = item_data.get('actual_qty', 0)
                item.save()
            except InventoryItem.DoesNotExist:
                continue

        return Response(self.get_serializer(inventory).data)

    @action(detail=True, methods=['post'])
    def apply(self, request, pk=None):
       
        inventory = self.get_object()
        if inventory.status != 'draft':
            return Response({"error": "Bu inventarizatsiya allaqachon tasdiqlangan!"}, status=status.HTTP_400_BAD_REQUEST)

        for item in inventory.items.all():
            product = item.product
            product.stock = item.actual_qty
            product.save()

        inventory.status = 'applied'
        inventory.applied_at = datetime.datetime.now()
        inventory.save()

        return Response(self.get_serializer(inventory).data)