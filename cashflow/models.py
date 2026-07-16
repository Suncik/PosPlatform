from django.db import models
from django.conf import settings


class CashMovement(models.Model):
    TYPE_CHOICES = [
        ('IN', "Kirim (naqd kirim)"),
        ('OUT', "Chiqim (kassa xarajat)"),
        ('COLLECTION', "Inkassatsiya (pul inkasso)"),
    ]
    movement_type = models.CharField(max_length=12, choices=TYPE_CHOICES, verbose_name="Turi")
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="Summa")
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name="Izoh")

    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name='cash_movements', null=True, blank=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kassa harakati"
        verbose_name_plural = "Kassa harakatlari"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.get_movement_type_display()} - {self.amount}"