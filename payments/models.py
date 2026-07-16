from django.db import models


class Kassa(models.Model):
  
    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name='kassalar', verbose_name="Do'kon")
    name = models.CharField(max_length=255, verbose_name="Kassa nomi")
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name="Balans")
    is_active = models.BooleanField(default=True, verbose_name="Holati")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Kassa"
        verbose_name_plural = "Kassalar"
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.store.name} — {self.name}"