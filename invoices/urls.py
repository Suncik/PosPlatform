from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StockReceiptViewSet

router = DefaultRouter()
router.register(r'list', StockReceiptViewSet, basename='stock-receipt')

urlpatterns = [
    path('', include(router.urls)),
]