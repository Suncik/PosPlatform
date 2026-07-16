from django.db import models
from django.db.models import Sum
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Debtor, DebtPayment
from .serializers import DebtorSerializer


class DebtorViewSet(viewsets.ModelViewSet):
    serializer_class = DebtorSerializer

    def get_queryset(self):
        qs = Debtor.objects.all().order_by('-created_at')
        search = self.request.query_params.get('search')
        if search:
            qs = qs.filter(models.Q(name__icontains=search) | models.Q(phone__icontains=search))
        return qs

    def perform_create(self, serializer):
        store = self.request.user.store if self.request.user.is_authenticated else None
        serializer.save(store=store)

    @action(detail=True, methods=['post'])
    def add_payment(self, request, pk=None):
        """ To'lov qabul qilish: POST /api/debts/list/{id}/add_payment/ { amount, comment } """
        debtor = self.get_object()
        amount = request.data.get('amount')

        try:
            amount = float(amount)
        except (TypeError, ValueError):
            return Response({"error": "To'lov summasi noto'g'ri"}, status=status.HTTP_400_BAD_REQUEST)

        if amount <= 0:
            return Response({"error": "Summa musbat bo'lishi kerak"}, status=status.HTTP_400_BAD_REQUEST)

        DebtPayment.objects.create(
            debtor=debtor,
            amount=amount,
            comment=request.data.get('comment'),
            created_by=request.user if request.user.is_authenticated else None,
        )
        return Response(DebtorSerializer(debtor).data, status=status.HTTP_200_OK)

    @action(detail=False, methods=['get'])
    def stats(self, request):
        """ Statistik kartochkalar: GET /api/debts/list/stats/ """
        debtors = self.get_queryset()
        total_debt = 0
        with_debt_count = 0
        for d in debtors:
            balance = d.current_balance
            if balance > 0:
                total_debt += float(balance)
                with_debt_count += 1

        return Response({
            "total_debt": total_debt,
            "debtors_count": debtors.count(),
            "with_debt_count": with_debt_count,
        })