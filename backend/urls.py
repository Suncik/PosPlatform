from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required
from .views import dashboard_page_loader

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='login.html'), name='login_page'),
    path('dashboard/', login_required(TemplateView.as_view(template_name='dashboard.html'), login_url='/'), name='dashboard_page'),
    path('pos/', login_required(TemplateView.as_view(template_name='pos.html'), login_url='/'), name='pos_page'),

    path('dashboard/pages/<str:page_key>/', dashboard_page_loader, name='dashboard_page_loader'),

    path('api/auth/', include('authentication.urls')),
    path('api/stores/', include('stores.urls')),
    path('api/suppliers/', include('suppliers.urls')),
    path('api/products/', include('products.urls')),
    path('api/sales/', include('sales.urls')),
    path('api/invoices/', include('invoices.urls')),
    path('api/debts/', include('debts.urls')),
    path('api/expenses/', include('expenses.urls')),
    path('api/payments/', include('payments.urls')),
    # backend/urls.py ga:
path('api/writeoffs/', include('writeoffs.urls')),
# backend/urls.py ga:
path('api/inventory/', include('inventory.urls')),
path('api/reports/', include('reports.urls')),
path('api/promotions/', include('promotions.urls')),
path('api/transfers/', include('transfers.urls')),
# backend/urls.py ga:
path('api/cashflow/', include('cashflow.urls')),
# backend/urls.py ga:
path('api/customers/', include('customers.urls')),
path('desktop-login/', TemplateView.as_view(template_name='desktop_login.html'), name='desktop_login_page'),
]