from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockTransferViewSet

router = DefaultRouter()
router.register(r'list', StockTransferViewSet, basename='transfer')

urlpatterns = [
    path('', include(router.urls)),
]