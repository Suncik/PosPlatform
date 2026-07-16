from rest_framework import viewsets
from .models import StockTransfer
from .serializers import StockTransferSerializer


class StockTransferViewSet(viewsets.ModelViewSet):
    serializer_class = StockTransferSerializer

    def get_queryset(self):
        return StockTransfer.objects.all().order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user if self.request.user.is_authenticated else None)