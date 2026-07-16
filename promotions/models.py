from django.db import models
from django.utils import timezone


class Promotion(models.Model):
    SCOPE_CHOICES = [
        ('ALL', 'Barcha mahsulotlar'),
        ('CATEGORY', 'Kategoriya bo\'yicha'),
        ('PRODUCT', 'Bitta mahsulot'),
    ]

    name = models.CharField(max_length=255, verbose_name="Nomi")
    discount_percent = models.DecimalField(max_digits=5, decimal_places=2, verbose_name="Chegirma foizi")

    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES, default='ALL', verbose_name="Qamrov")
    category = models.ForeignKey('products.Category', on_delete=models.SET_NULL, null=True, blank=True, related_name="promotions")
    product = models.ForeignKey('products.Product', on_delete=models.SET_NULL, null=True, blank=True, related_name="promotions")

    start_date = models.DateField(verbose_name="Boshlanish")
    end_date = models.DateField(verbose_name="Tugash")

    is_active = models.BooleanField(default=True, verbose_name="Faol (qo'lda o'chirilmagan)")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Aksiya"
        verbose_name_plural = "Aksiyalar"
        ordering = ['-created_at']

    @property
    def status(self):
        today = timezone.now().date()
        if not self.is_active:
            return "CANCELLED"
        if today > self.end_date:
            return "ENDED"
        if today < self.start_date:
            return "UPCOMING"
        return "ACTIVE"

    def __str__(self):
        return self.name