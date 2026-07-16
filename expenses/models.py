from django.db import models
from django.conf import settings


class Expense(models.Model):
   
    name = models.CharField(max_length=255, verbose_name="Nomi")
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Summa")
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name="Izoh")

    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name="expenses", null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Sana")

    class Meta:
        verbose_name = "Xarajat"
        verbose_name_plural = "Xarajatlar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name} - {self.amount}"