from rest_framework import viewsets
from .models import Sale
from .serializers import SaleSerializer
from datetime import datetime as dt
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import Shift, Sale, SaleItem
from decimal import Decimal
from .serializers import ShiftSerializer
from django.db.models import Sum, Count, Q
from datetime import date
from django_filters.rest_framework import DjangoFilterBackend
from expenses.models import Expense
from decimal import Decimal
from datetime import timedelta, datetime as dt
from django.db.models.functions import TruncDate
from .models import Shift, Sale, SaleItem


class DailySalesView(viewsets.ViewSet):
   
    def list(self, request):
        date_str = request.query_params.get('date')
        if date_str:
            try:
                target_date = dt.strptime(date_str, '%Y-%m-%d').date()
            except ValueError:
                return Response({"error": "Sana formati noto'g'ri (YYYY-MM-DD kerak)"}, status=status.HTTP_400_BAD_REQUEST)
        else:
            target_date = date.today()

        day_sales = Sale.objects.filter(created_at__date=target_date).order_by('-created_at')

        cash_total = day_sales.aggregate(total=Sum('paid_cash'))['total'] or 0
        card_total = day_sales.aggregate(total=Sum('paid_card'))['total'] or 0
        credit_total = day_sales.filter(payment_method='CREDIT').aggregate(total=Sum('total_amount'))['total'] or 0
        net_total = day_sales.aggregate(total=Sum('total_amount'))['total'] or 0

        sales_list = [
            {
                "id": s.id,
                "payment_method": s.payment_method,
                "payment_method_display": s.get_payment_method_display(),
                "created_at": s.created_at,
                "total_amount": float(s.total_amount),
                "store_name": s.store.name if s.store else '—',
            }
            for s in day_sales
        ]

        return Response({
            "date": target_date.isoformat(),
            "total_sales": day_sales.count(),
            "cash_income": float(cash_total),
            "card_income": float(card_total),
            "credit_income": float(credit_total),
            "returns": 0,
            "net_income": float(net_total),
            "sales": sales_list,
        })


def build_shift_report(shift):
 
    sales_qs = Sale.objects.filter(shift=shift)

    sotuv_operatsiyalari = sales_qs.count()
    sotilgan_tovarlar = SaleItem.objects.filter(sale__shift=shift).aggregate(total=Sum('quantity'))['total'] or 0
    sotuv_jami = sales_qs.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
    naqd_sof = sales_qs.aggregate(total=Sum('paid_cash'))['total'] or Decimal('0.00')
    karta_sof = sales_qs.aggregate(total=Sum('paid_card'))['total'] or Decimal('0.00')

    qqs = sotuv_jami * Decimal('12') / Decimal('112')

    boshlangich = shift.opening_balance or Decimal('0.00')
    kutilgan_naqd = boshlangich + naqd_sof
    sanalgan_naqd = shift.closing_balance if shift.closing_balance is not None else Decimal('0.00')
    farq = sanalgan_naqd - kutilgan_naqd

    return {
        "shift_id": shift.id,
        "cashier_name": shift.cashier.full_name if shift.cashier else '—',
        "opened_at": shift.opened_at,
        "closed_at": shift.closed_at,
        "is_open": shift.is_open,
        "sotuv_operatsiyalari": sotuv_operatsiyalari,
        "sotilgan_tovarlar": float(sotilgan_tovarlar),
        "sotuv_jami": float(sotuv_jami),
        "qqs": float(qqs),
        "naqd_sof": float(naqd_sof),
        "karta_sof": float(karta_sof),
        "boshlangich_naqd": float(boshlangich),
        "kutilgan_naqd": float(kutilgan_naqd),
        "sanalgan_naqd": float(sanalgan_naqd),
        "farq": float(farq),
    }


class ShiftViewSet(viewsets.ModelViewSet):
    queryset = Shift.objects.all().order_by('-opened_at')
    serializer_class = ShiftSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role and user.role.name != "Admin":
            return Shift.objects.filter(cashier=user).order_by('-opened_at')
        return Shift.objects.all().order_by('-opened_at')

    @action(detail=False, methods=['get'])
    def current(self, request):
      
        if not request.user.is_authenticated:
            return Response({"error": "Tizimga kirilmagan"}, status=status.HTTP_401_UNAUTHORIZED)
        shift = Shift.objects.filter(cashier=request.user, is_open=True).order_by('-opened_at').first()
        if not shift:
            return Response({}, status=status.HTTP_200_OK)
        return Response(ShiftSerializer(shift).data)

    @action(detail=False, methods=['post'])
    def open_shift(self, request):

        if not request.user.is_authenticated:
            return Response({"error": "Tizimga kirilmagan"}, status=status.HTTP_401_UNAUTHORIZED)
        if Shift.objects.filter(cashier=request.user, is_open=True).exists():
            return Response({"error": "Sizda allaqachon ochiq smena mavjud!"}, status=status.HTTP_400_BAD_REQUEST)

        if not request.user.store:
            return Response({"error": "Sizga hali do'kon biriktirilmagan!"}, status=status.HTTP_400_BAD_REQUEST)

        shift = Shift.objects.create(
            store=request.user.store,
            cashier=request.user,
            opening_balance=request.data.get('opening_balance', 0),
        )
        return Response(ShiftSerializer(shift).data, status=status.HTTP_201_CREATED)

    @action(detail=True, methods=['post'])
    def close_shift(self, request, pk=None):
        shift = self.get_object()
        if not shift.is_open:
            return Response({"error": "Bu smena allaqachon yopilgan!"}, status=status.HTTP_400_BAD_REQUEST)

        shift.closing_balance = request.data.get('closing_balance', 0.00)
        shift.is_open = False
        import datetime
        shift.closed_at = datetime.datetime.now()
        shift.save()

        return Response(build_shift_report(shift), status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'])
    def report(self, request, pk=None):
        """Smena hisoboti (X/Z): GET /api/sales/shifts/{id}/report/"""
        shift = self.get_object()
        return Response(build_shift_report(shift))


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all().order_by('-created_at')
    serializer_class = SaleSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['store', 'cashier', 'payment_method']

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated and user.role and user.role.name != "Admin":
            return Sale.objects.filter(store=user.store).order_by('-created_at')
        return Sale.objects.all().order_by('-created_at')


class DashboardStatsView(viewsets.ViewSet):
  
    def list(self, request):
        today = date.today()

      
        today_sales = Sale.objects.filter(created_at__date=today)

        total_sales = today_sales.count()
        cash_income = today_sales.aggregate(total=Sum('paid_cash'))['total'] or 0
        card_income = today_sales.aggregate(total=Sum('paid_card'))['total'] or 0

        
        today_expenses = Expense.objects.filter(created_at__date=today).aggregate(total=Sum('amount'))['total'] or 0

        data = {
            "total_sales": total_sales,
            "cash_income": float(cash_income),
            "card_income": float(card_income),
            "returns": 0,      # Hozircha Return modeli yo'q
            "debts": 0,        # Hozircha Debt modeli yo'q
            "expenses": float(today_expenses),
        }
        return Response(data)
    

class AnalyticsView(viewsets.ViewSet):
  
    def list(self, request):
        date_from_str = request.query_params.get('date_from')
        date_to_str = request.query_params.get('date_to')

        try:
            date_from = dt.strptime(date_from_str, '%Y-%m-%d').date() if date_from_str else date.today() - timedelta(days=6)
            date_to = dt.strptime(date_to_str, '%Y-%m-%d').date() if date_to_str else date.today()
        except ValueError:
            return Response({"error": "Sana formati noto'g'ri (YYYY-MM-DD kerak)"}, status=status.HTTP_400_BAD_REQUEST)

        sales_qs = Sale.objects.filter(created_at__date__gte=date_from, created_at__date__lte=date_to)

        tushum = sales_qs.aggregate(total=Sum('total_amount'))['total'] or Decimal('0.00')
        savdolar = sales_qs.count()

        items_qs = SaleItem.objects.filter(sale__in=sales_qs).select_related('product')


        tannarx = Decimal('0.00')
        for item in items_qs:
            tannarx += item.quantity * (item.product.cost_price or Decimal('0.00'))

        foyda = tushum - tannarx
        marja = float(foyda / tushum * 100) if tushum > 0 else 0
        average_check = float(tushum / savdolar) if savdolar > 0 else 0

        
        daily = (
            sales_qs.annotate(day=TruncDate('created_at'))
            .values('day')
            .annotate(total=Sum('total_amount'))
            .order_by('day')
        )
        daily_sales = [
            {"date": d['day'].isoformat(), "label": d['day'].strftime('%d/%m'), "total": float(d['total'])}
            for d in daily
        ]

        
        top_products = (
            items_qs.values('product__name')
            .annotate(qty=Sum('quantity'), revenue=Sum('total_price'))
            .order_by('-revenue')[:10]
        )
        top_products_list = [
            {"name": p['product__name'], "qty": float(p['qty']), "revenue": float(p['revenue'])}
            for p in top_products
        ]

        return Response({
            "date_from": date_from.isoformat(),
            "date_to": date_to.isoformat(),
            "tushum": float(tushum),
            "tannarx": float(tannarx),
            "foyda": float(foyda),
            "marja": round(marja, 1),
            "savdolar": savdolar,
            "average_check": round(average_check),
            "daily_sales": daily_sales,
            "top_products": top_products_list,
        })