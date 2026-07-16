from django.shortcuts import render
from django.http import Http404
from django.contrib.auth.decorators import login_required

ALLOWED_PAGES = {
    'stores', 'products', 'categories', 'sales', 'shifts',
    'suppliers', 'invoices', 'debts', 'expenses',
    'payments', 'writeoffs', 'inventory', 'analytics', 'reports',
    'promotions', 'transfer', 'cashflow', 'customers',
    'users', 'roles', 'settings',
}

@login_required
def dashboard_page_loader(request, page_key):
    if page_key not in ALLOWED_PAGES:
        raise Http404("Bunday sahifa mavjud emas")
    return render(request, f'pages/{page_key}.html')