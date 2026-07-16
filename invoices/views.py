from rest_framework import viewsets
from .models import StockReceipt
from .serializers import StockReceiptSerializer


class StockReceiptViewSet(viewsets.ModelViewSet):
    serializer_class = StockReceiptSerializer

    def get_queryset(self):
        user = self.request.user
        qs = StockReceipt.objects.all().order_by('-created_at')
        if user.is_authenticated and user.role and user.role.name != "Admin":
            qs = qs.filter(store=user.store)
        return qs

    def perform_create(self, serializer):
        serializer.save(store=self.request.user.store, created_by=self.request.user)