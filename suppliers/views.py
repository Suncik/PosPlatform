from django.db import models
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Supplier
from .serializers import SupplierSerializer


class SupplierViewSet(viewsets.ModelViewSet):
    serializer_class = SupplierSerializer

    def get_queryset(self):
        queryset = Supplier.objects.all().order_by('-created_at')
        search = self.request.query_params.get('search')
        if search:
            queryset = queryset.filter(
                models.Q(name__icontains=search) | models.Q(phone__icontains=search)
            )
        return queryset

    @action(detail=True, methods=['post'])
    def toggle_active(self, request, pk=None):
        """ Aktiv/O'chiq holatini almashtiradi: POST /api/suppliers/list/{id}/toggle_active/ """
        supplier = self.get_object()
        supplier.is_active = not supplier.is_active
        supplier.save()
        return Response(SupplierSerializer(supplier).data, status=status.HTTP_200_OK)