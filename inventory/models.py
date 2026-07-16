from django.db import models
from django.conf import settings


class Inventory(models.Model):
    STATUS_CHOICES = [
        ('draft', 'Qoralama'),
        ('applied', 'Tasdiqlangan'),
    ]
    number = models.CharField(max_length=50, unique=True, verbose_name="Raqami")
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name='inventories', null=True, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    applied_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Inventarizatsiya"
        verbose_name_plural = "Inventarizatsiyalar"
        ordering = ['-created_at']

    def __str__(self):
        return self.number


class InventoryItem(models.Model):
    inventory = models.ForeignKey(Inventory, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    expected_qty = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Kutilgan")
    actual_qty = models.DecimalField(max_digits=10, decimal_places=3, default=0, verbose_name="Haqiqiy")