from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import StoreViewSet, SystemSettingsAPIView

router = DefaultRouter()
router.register(r'list', StoreViewSet, basename='store')

urlpatterns = [
    path('', include(router.urls)),
    path('settings/', SystemSettingsAPIView.as_view(), name='system-settings'),
]