# apps/users/models.py
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone

class Empresa(models.Model):
    nombre = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nombre

class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, cedula, email, password, **extra_fields):
        if not cedula:
            raise ValueError('La cédula es obligatoria.')
        if not email:
            raise ValueError('El correo es obligatorio.')
        cedula = str(cedula)
        email = self.normalize_email(email)
        user = self.model(cedula=cedula, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, cedula, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(cedula, email, password, **extra_fields)

    def create_superuser(self, cedula, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('rol', 'Gerente')
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self._create_user(cedula, email, password, **extra_fields)

class Rol(models.Model):
    nombre_rol = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.nombre_rol


class User(AbstractUser):
    # quitamos username requerido; usamos cedula como identificador
    username = models.CharField(max_length=150, blank=True, null=True)
    cedula = models.CharField(max_length=20, unique=True)
   
    rol = models.ForeignKey(Rol, on_delete=models.SET_NULL, null=True)
    email = models.EmailField('Correo electrónico', unique=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.SET_NULL, null=True, blank=True)
    # control para recuperación: cuando se asigna contraseña temporal = True -> forzar cambio
    is_temp_password = models.BooleanField(default=False)
    # quedamos con is_active (ya incluye bloqueo)
    date_joined = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'cedula'
    REQUIRED_FIELDS = ['email']

    objects = UserManager()

    def __str__(self):
        nombre = f"{self.first_name} {self.last_name}".strip()
        return f"{nombre or self.cedula} ({self.rol})"

