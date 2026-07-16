from django.db import models
from django.conf import settings
import uuid


class StockReceipt(models.Model):
   
    number = models.CharField(max_length=50, unique=True, editable=False, verbose_name="Hujjat raqami")
    supplier = models.ForeignKey('suppliers.Supplier', on_delete=models.SET_NULL, null=True, related_name="receipts", verbose_name="Yetkazib beruvchi")
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name="receipts", verbose_name="Do'kon")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name="receipts")
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name="Izoh")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "Накладная"
        verbose_name_plural = "Накладные"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f"KIRIM-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.number


class StockReceiptItem(models.Model):
    
    receipt = models.ForeignKey(StockReceipt, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name="stock_receipt_items")

    quantity = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Miqdor")
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tannarx")
    batch_number = models.CharField(max_length=100, blank=True, null=True, verbose_name="Partiya №")
    expiry_date = models.DateField(blank=True, null=True, verbose_name="Muddati")

    line_total = models.DecimalField(max_digits=14, decimal_places=2, default=0, editable=False)

    def save(self, *args, **kwargs):
        self.line_total = self.quantity * self.cost_price
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"