from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import KassaViewSet

router = DefaultRouter()
router.register(r'list', KassaViewSet, basename='kassa')

urlpatterns = [
    path('', include(router.urls)),
]