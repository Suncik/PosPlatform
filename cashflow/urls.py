from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import CashMovementViewSet

router = DefaultRouter()
router.register(r'list', CashMovementViewSet, basename='cashmovement')

urlpatterns = [
    path('', include(router.urls)),
]