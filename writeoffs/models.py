from django.db import models
from django.conf import settings


class WriteOff(models.Model):
  
    reason = models.CharField(max_length=500, verbose_name="Sabab")
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name='writeoffs', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Hisobdan chiqarish"
        verbose_name_plural = "Hisobdan chiqarishlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"№{self.id} — {self.reason}"


class WriteOffItem(models.Model):
   
    writeoff = models.ForeignKey(WriteOff, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.DecimalField(max_digits=10, decimal_places=3, verbose_name="Miqdor")
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, verbose_name="Tannarx (o'sha paytdagi)")