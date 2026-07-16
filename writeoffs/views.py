from django.db import transaction
from rest_framework import viewsets, status
from rest_framework.response import Response
from products.models import Product
from .models import WriteOff, WriteOffItem
from .serializers import WriteOffSerializer


class WriteOffViewSet(viewsets.ModelViewSet):
    serializer_class = WriteOffSerializer

    def get_queryset(self):
        user = self.request.user
        qs = WriteOff.objects.all().order_by('-created_at')
        if user.is_authenticated and user.role and user.role.name != "Admin":
            qs = qs.filter(store=user.store)
        return qs

    @transaction.atomic
    def create(self, request, *args, **kwargs):
        reason = (request.data.get('reason') or '').strip()
        items_data = request.data.get('items', [])

        if not reason:
            return Response({"error": "Sababni kiriting!"}, status=status.HTTP_400_BAD_REQUEST)
        if not items_data:
            return Response({"error": "Kamida bitta tovar qo'shing!"}, status=status.HTTP_400_BAD_REQUEST)

        user = request.user
        writeoff = WriteOff.objects.create(
            reason=reason,
            store=user.store if user.is_authenticated else None,
            created_by=user if user.is_authenticated else None,
        )

        for item in items_data:
            try:
                product = Product.objects.get(id=item.get('product_id'))
            except Product.DoesNotExist:
                return Response({"error": f"Mahsulot topilmadi (ID: {item.get('product_id')})"}, status=status.HTTP_400_BAD_REQUEST)

            try:
                quantity = float(item.get('quantity', 0))
            except (TypeError, ValueError):
                quantity = 0

            if quantity <= 0:
                continue

            WriteOffItem.objects.create(
                writeoff=writeoff,
                product=product,
                quantity=quantity,
                cost_price=product.cost_price,
            )

            
            product.stock = max(0, product.stock - quantity)
            product.save()

        serializer = self.get_serializer(writeoff)
        return Response(serializer.data, status=status.HTTP_201_CREATED)