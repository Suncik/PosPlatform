from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Promotion
from .serializers import PromotionSerializer


class PromotionViewSet(viewsets.ModelViewSet):
    queryset = Promotion.objects.all().order_by('-created_at')
    serializer_class = PromotionSerializer

    @action(detail=True, methods=['post'])
    def deactivate(self, request, pk=None):
       
        promo = self.get_object()
        promo.is_active = False
        promo.save()
        return Response(PromotionSerializer(promo).data, status=status.HTTP_200_OK)