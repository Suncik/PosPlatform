from django.db import models
from django.conf import settings
from decimal import Decimal


class Shift(models.Model):
 
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name="shifts")
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="shifts")
    
    opened_at = models.DateTimeField(auto_now_add=True, verbose_name="Smena ochilgan vaqti")
    closed_at = models.DateTimeField(null=True, blank=True, verbose_name="Smena yopilgan vaqti")
    
    opening_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Ochilishdagi pul (Kassa)")
    closing_balance = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True, verbose_name="Yopilishdagi pul")
    
    is_open = models.BooleanField(default=True, verbose_name="Smena holati")

    class Meta:
        verbose_name = "Smena"
        verbose_name_plural = "Smenalar"

    def __str__(self):
        return f"{self.cashier.full_name} - Smena #{self.id} ({'Ochiq' if self.is_open else 'Yopilgan'})"

class Sale(models.Model):
   
    PAYMENT_METHODS = [
    ('CASH', 'Naqd'),
    ('CARD', 'Plastik Karta'),
    ('MIXED', 'Aralash (Naqd + Karta)'),
    ('CREDIT', 'Nasiya'),
]

    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name="sales", verbose_name="Do'kon")
    cashier = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="sales", verbose_name="Kassir")
    # buni Sale modelining ichiga qo'shib qo'ying:
    shift = models.ForeignKey(Shift, on_delete=models.SET_NULL, null=True, blank=True, related_name="sales")
    total_amount = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Umumiy summa")
    paid_cash = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Naqd to'lov")
    paid_card = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Karta orqali to'lov")
    
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS, default='CASH', verbose_name="To'lov turi")
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sotilgan vaqti")

    class Meta:
        verbose_name = "Savdo"
        verbose_name_plural = "Savdolar"

    def __str__(self):
        return f"Chek #{self.id} - {self.total_amount} {self.store.name}"


class SaleItem(models.Model):
  
    sale = models.ForeignKey(Sale, on_delete=models.CASCADE, related_name="items", verbose_name="Chek")
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name="sale_items", verbose_name="Mahsulot")
    
    quantity = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Miqdori (Dona/Kg)")
    price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Sotilgan narxi")
    total_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Jami narxi")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"

    def save(self, *args, **kwargs):
  
        self.total_price = Decimal(str(self.quantity)) * Decimal(str(self.price))
        super().save(*args, **kwargs)
        
