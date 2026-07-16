from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin

class CustomUserManager(BaseUserManager):
    def create_user(self, phone, username, password=None, **extra_fields):
        if not phone:
            raise ValueError("Telefon raqami kiritilishi shart!")
        if not username:
            raise ValueError("Foydalanuvchi nomi (username) kiritilishi shart!")
        
        extra_fields.setdefault('is_active', True)
        user = self.model(phone=phone, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(phone, username, password, **extra_fields)


class Role(models.Model):
    """
    Rollar jadvali (Admin, Kassir, Menejer va h.k.)
    """
    name = models.CharField(max_length=100, unique=True, verbose_name="Rol nomi")
    is_system = models.BooleanField(default=False, verbose_name="Tizim roli")
    permissions = models.JSONField(default=dict, blank=True, verbose_name="Ruxsatlar")
    is_active = models.BooleanField(default=True, verbose_name="Holati")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class User(AbstractBaseUser, PermissionsMixin):
    """
    Kengaytirilgan maxsus Foydalanuvchi modeli
    """
    username = models.CharField(max_length=150, unique=True, verbose_name="Foydalanuvchi nomi")
    full_name = models.CharField(max_length=255, verbose_name="Foydalanuvchi F.I.O")
    phone = models.CharField(max_length=20, unique=True, verbose_name="Telefon raqami")
    
    # Biz yaratgan Rol modeliga bog'liqlik# TO'G'RI VARIANT
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True, related_name="users")
    store = models.ForeignKey('stores.Store', on_delete=models.SET_NULL, null=True, blank=True, related_name="staff")
    
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['phone']

    def __str__(self):
        return f"{self.full_name} ({self.role.name if self.role else 'Rol berilmagan'})"