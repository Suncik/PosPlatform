from django.db import models


class Supplier(models.Model):
   
    name = models.CharField(max_length=255, verbose_name="Nomi")
    contact_person = models.CharField(max_length=255, blank=True, null=True, verbose_name="Mas'ul shaxs")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon")
    address = models.CharField(max_length=500, blank=True, null=True, verbose_name="Manzil")

    is_active = models.BooleanField(default=True, verbose_name="Holati")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Yetkazib beruvchi"
        verbose_name_plural = "Yetkazib beruvchilar"

    def __str__(self):
        return self.name