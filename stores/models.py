from django.db import models

class Store(models.Model):
    
    ACTIVITY_CHOICES = [
        ('dokon', "🏪 Do'kon"),
        ('restoran', "🍽️ Restoran"),
    ]
   
    name = models.CharField(max_length=255, verbose_name="Do'kon/Filial nomi")
    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name="Telefon raqami")
    address = models.TextField(blank=True, null=True, verbose_name="Manzili")
    activity_type = models.CharField(max_length=20, choices=ACTIVITY_CHOICES, default='dokon', verbose_name="Faoliyat turi")
    balance = models.DecimalField(max_digits=14, decimal_places=2, default=0.00, verbose_name="Balans")
    is_active = models.BooleanField(default=True, verbose_name="Holati")
    
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    def __str__(self):
        return self.name


class SystemSettings(models.Model):
  
    company_name = models.CharField(max_length=255, verbose_name="Kompaniya nomi")
    phone = models.CharField(max_length=20, verbose_name="Telefon")
    tax_percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0.00, verbose_name="Soliq (%)")
    currency = models.CharField(max_length=10, default="SO'M", verbose_name="Valyuta")
    address = models.TextField(blank=True, null=True, verbose_name="Manzil")
    
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tizim sozlamasi"
        verbose_name_plural = "Tizim sozlamalari"

    def __str__(self):
        return self.company_name

    def save(self, *args, **kwargs):
     
        if not self.pk and SystemSettings.objects.exists():
            return
        super().save(*args, **kwargs)