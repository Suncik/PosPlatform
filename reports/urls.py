from django.urls import path
from .views import SalesReportView, StockReportView

urlpatterns = [
    path('sales/', SalesReportView.as_view(), name='report-sales'),
    path('stock/', StockReportView.as_view(), name='report-stock'),
]