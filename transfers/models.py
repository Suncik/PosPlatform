from django.db import models
from django.conf import settings
import uuid


class StockTransfer(models.Model):
    STATUS_CHOICES = [
        ('COMPLETED', 'Bajarildi'),
        ('CANCELLED', 'Bekor qilindi'),
    ]

    number = models.CharField(max_length=50, unique=True, editable=False, verbose_name="Raqam")
    source_store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name="transfers_out", verbose_name="Manba filial")
    destination_store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name="transfers_in", verbose_name="Maqsad filial")
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name="Izoh")
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='COMPLETED')

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "Transfer"
        verbose_name_plural = "Transferlar"
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.number:
            self.number = f"TRANSFER-{uuid.uuid4().hex[:8]}"
        super().save(*args, **kwargs)

    def __str__(self):
        return self.number


class StockTransferItem(models.Model):
    transfer = models.ForeignKey(StockTransfer, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey('products.Product', on_delete=models.PROTECT, related_name="transfer_items")
    quantity = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Miqdor")

    def __str__(self):
        return f"{self.product.name} x {self.quantity}"