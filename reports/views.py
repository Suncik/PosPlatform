from datetime import datetime
from django.db import models
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from rest_framework.views import APIView
from rest_framework.response import Response
from sales.models import Sale, SaleItem
from products.models import Product


class SalesReportView(APIView):


    def get(self, request):
        date_from_str = request.query_params.get('date_from')
        date_to_str = request.query_params.get('date_to')

        try:
            date_from = datetime.strptime(date_from_str, '%Y-%m-%d').date() if date_from_str else datetime.today().date()
            date_to = datetime.strptime(date_to_str, '%Y-%m-%d').date() if date_to_str else datetime.today().date()
        except ValueError:
            return Response({"error": "Sana formati noto'g'ri"}, status=400)

        sales_qs = Sale.objects.filter(created_at__date__gte=date_from, created_at__date__lte=date_to)

        user = request.user
        if user.is_authenticated and user.role and user.role.name != "Admin":
            sales_qs = sales_qs.filter(store=user.store)

        jami_tushum = sales_qs.aggregate(t=Sum('total_amount'))['t'] or 0
        naqd = sales_qs.aggregate(t=Sum('paid_cash'))['t'] or 0
        karta = sales_qs.aggregate(t=Sum('paid_card'))['t'] or 0
        nasiya = sales_qs.filter(payment_method='CREDIT').aggregate(t=Sum('total_amount'))['t'] or 0
        savdolar_soni = sales_qs.count()

     
        items_qs = SaleItem.objects.filter(sale__in=sales_qs).select_related('product')
        tannarx = sum(float(i.quantity) * float(i.product.cost_price) for i in items_qs)

        jami_tushum_f = float(jami_tushum)
        foyda = jami_tushum_f - tannarx
        marjinallik = (foyda / jami_tushum_f * 100) if jami_tushum_f else 0

        daily = sales_qs.annotate(day=TruncDate('created_at')).values('day').annotate(
            savdolar=Count('id'), tushum=Sum('total_amount')
        ).order_by('day')

        daily_list = []
        for row in daily:
            day_items = SaleItem.objects.filter(
                sale__created_at__date=row['day'], sale__in=sales_qs
            ).select_related('product')
            day_cost = sum(float(i.quantity) * float(i.product.cost_price) for i in day_items)
            day_tushum = float(row['tushum'] or 0)
            daily_list.append({
                "date": row['day'].isoformat(),
                "sales_count": row['savdolar'],
                "income": day_tushum,
                "cost": day_cost,
                "profit": day_tushum - day_cost,
            })

        return Response({
            "jami_tushum": jami_tushum_f,
            "tannarx": tannarx,
            "foyda": foyda,
            "marjinallik": round(marjinallik, 1),
            "savdolar_soni": savdolar_soni,
            "qaytarishlar": 0,
            "naqd": float(naqd),
            "karta": float(karta),
            "nasiya": float(nasiya),
            "daily": daily_list,
        })


class StockReportView(APIView):


    def get(self, request):
        search = request.query_params.get('search')
        qs = Product.objects.filter(is_active=True).select_related('category')

        user = request.user
        if user.is_authenticated and user.role and user.role.name != "Admin":
            qs = qs.filter(store=user.store)
        if search:
            qs = qs.filter(models.Q(name__icontains=search) | models.Q(barcode__icontains=search))

        total_cost_value = 0
        total_sale_value = 0
        products_list = []

        for p in qs:
            cost_val = float(p.stock) * float(p.cost_price)
            sale_val = float(p.stock) * float(p.selling_price)
            total_cost_value += cost_val
            total_sale_value += sale_val
            products_list.append({
                "name": p.name,
                "category_name": p.category.name if p.category else "—",
                "barcode": p.barcode,
                "stock": float(p.stock),
                "unit": p.unit,
                "cost_price": float(p.cost_price),
                "selling_price": float(p.selling_price),
                "cost_value": cost_val,
                "sale_value": sale_val,
            })

        return Response({
            "total_products": len(products_list),
            "total_cost_value": total_cost_value,
            "total_sale_value": total_sale_value,
            "products": products_list,
        })