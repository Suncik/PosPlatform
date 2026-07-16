from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Expense
from .serializers import ExpenseSerializer


class ExpenseViewSet(viewsets.ModelViewSet):
    serializer_class = ExpenseSerializer

    def get_queryset(self):
        user = self.request.user
        qs = Expense.objects.all().order_by('-created_at')
        if user.is_authenticated and user.role and user.role.name != "Admin":
            qs = qs.filter(store=user.store)
        return qs

    def perform_create(self, serializer):
        store = self.request.user.store if self.request.user.is_authenticated else None
        serializer.save(store=store, created_by=self.request.user if self.request.user.is_authenticated else None)

    @action(detail=False, methods=['get'])
    def total(self, request):
        """ GET /api/expenses/list/total/ """
        total = self.get_queryset().aggregate(t=Sum('amount'))['t'] or 0
        return Response({"total": float(total)})