from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=255, verbose_name="Ismi")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    email = models.EmailField(blank=True, null=True, verbose_name="Email")
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="Manzil")
    comment = models.CharField(max_length=500, blank=True, null=True, verbose_name="Izoh")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Chegirma (%)")
    points = models.PositiveIntegerField(default=0, verbose_name="Ball")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Mijoz"
        verbose_name_plural = "Mijozlar"
        ordering = ['-created_at']

    def __str__(self):
        return self.name