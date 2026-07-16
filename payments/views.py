from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from .models import Kassa
from .serializers import KassaSerializer


class KassaViewSet(viewsets.ModelViewSet):
    queryset = Kassa.objects.all().order_by('-created_at')
    serializer_class = KassaSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store', 'is_active']