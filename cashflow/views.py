from django.db.models import Sum
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import CashMovement
from .serializers import CashMovementSerializer


class CashMovementViewSet(viewsets.ModelViewSet):
    serializer_class = CashMovementSerializer

    def get_queryset(self):
        user = self.request.user
        qs = CashMovement.objects.all().order_by('-created_at')
        if user.is_authenticated and user.role and user.role.name != "Admin":
            qs = qs.filter(store=user.store)
        return qs

    def perform_create(self, serializer):
        store = self.request.user.store if self.request.user.is_authenticated else None
        serializer.save(store=store, created_by=self.request.user if self.request.user.is_authenticated else None)

    @action(detail=False, methods=['get'])
    def totals(self, request):
        """ GET /api/cashflow/list/totals/ """
        qs = self.get_queryset()
        kirim = qs.filter(movement_type='IN').aggregate(t=Sum('amount'))['t'] or 0
        chiqim = qs.filter(movement_type__in=['OUT', 'COLLECTION']).aggregate(t=Sum('amount'))['t'] or 0
        return Response({"kirim": float(kirim), "chiqim": float(chiqim)})