from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import DebtorViewSet

router = DefaultRouter()
router.register(r'list', DebtorViewSet, basename='debtor')

urlpatterns = [
    path('', include(router.urls)),
]   