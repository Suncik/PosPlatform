from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'transactions', SaleViewSet, basename='sale')
router.register(r'shifts', ShiftViewSet, basename='shift')

urlpatterns = [
    path('dashboard-stats/', DashboardStatsView.as_view({'get': 'list'}), name='dashboard-stats'),
      path('daily-sales/', DailySalesView.as_view({'get': 'list'}), name='daily-sales'),
      path('analytics/', AnalyticsView.as_view({'get': 'list'}), name='analytics'),
    path('', include(router.urls)),
]