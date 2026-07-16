from django.db import models
from django.conf import settings


class Debtor(models.Model):
   
    name = models.CharField(max_length=255, verbose_name="Ism")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name="Izoh")
    initial_debt = models.DecimalField(max_digits=14, decimal_places=2, default=0, verbose_name="Boshlang'ich qarz")

    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name="debtors", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Qarzdor"
        verbose_name_plural = "Qarzdorlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def current_balance(self):
        paid = self.payments.aggregate(total=models.Sum('amount'))['total'] or 0
        return self.initial_debt - paid


class DebtPayment(models.Model):
   
    debtor = models.ForeignKey(Debtor, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=14, decimal_places=2, verbose_name="To'lov summasi")
    comment = models.CharField(max_length=500, blank=True, null=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.debtor.name} - {self.amount}"