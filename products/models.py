from django.db import models

class Category(models.Model):
   
    name = models.CharField(max_length=255, unique=True, verbose_name="Kategoriya nomi")
    description = models.TextField(blank=True, null=True, verbose_name="Izoh")
    is_active = models.BooleanField(default=True, verbose_name="Holati")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Kategoriya"
        verbose_name_plural = "Kategoriyalar"

    def __str__(self):
        return self.name


class Product(models.Model):
    
    UNIT_CHOICES = [
        ('dona', 'Dona'),
        ('kg', 'Kilogramm'),
        ('litr', 'Litr'),
        ('metr', 'Metr'),
        ('quti', 'Quti'),
    ]
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name="products", verbose_name="Kategoriyasi")
    name = models.CharField(max_length=255, verbose_name="Mahsulot nomi")
    

    barcode = models.CharField(max_length=50, unique=True, blank=True, null=True, verbose_name="Shtrix-kod")
    plu = models.CharField(max_length=50, blank=True, null=True, verbose_name="PLU kod")                     
    description = models.TextField(blank=True, null=True, verbose_name="Tavsif")                              
    unit = models.CharField(max_length=10, choices=UNIT_CHOICES, default='dona', verbose_name="Birlik")        
    has_vat = models.BooleanField(default=True, verbose_name="НДС")                                            
    has_marking = models.BooleanField(default=False, verbose_name="Markirovka")                                
    supplier_name = models.CharField(max_length=255, blank=True, null=True, verbose_name="Yetkazib beruvchi")
    
    
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Tannarxi")
    selling_price = models.DecimalField(max_digits=12, decimal_places=2, default=0.00, verbose_name="Sotish narxi")
    
    
    stock = models.DecimalField(max_digits=10, decimal_places=3, default=0.000, verbose_name="Ombordagi qoldiq")
    is_weighted = models.BooleanField(default=False, verbose_name="Vaznli mahsulot (Kg/Litr)") 
    

    store = models.ForeignKey('stores.Store', on_delete=models.CASCADE, related_name="products", verbose_name="Do'kon")
    
    is_active = models.BooleanField(default=True, verbose_name="Holati")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Mahsulot"
        verbose_name_plural = "Mahsulotlar"
     
        unique_together = ('store', 'barcode')

    def __str__(self):
        return f"{self.name} - ({self.store.name})"