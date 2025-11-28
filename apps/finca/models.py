from django.db import models
from django.core.exceptions import ValidationError

class Finca(models.Model):
    id = models.BigAutoField(primary_key=True)
    nombre = models.CharField(max_length=200, unique=True)
    ubicacion = models.CharField(max_length=300, blank=True)
    codigo = models.CharField(max_length=50, unique=True)
    propietario = models.CharField(max_length=200, blank=True)
    telefono_contacto = models.CharField(max_length=20, blank=True)

    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['nombre']
        verbose_name = 'Finca'
        verbose_name_plural = 'Fincas'

    def __str__(self):
        return f"{self.nombre} ({self.codigo})"

    def clean(self):
        if len(self.codigo) < 3:
            raise ValidationError("El código de la finca debe tener al menos 3 caracteres.")
        super().clean()
