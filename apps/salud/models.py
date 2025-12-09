from django.db import models
from apps.ganaderia.models import Animal
from apps.users.models import User
 


class EventoSanitario(models.Model):
    fecha = models.DateField()
    diagnostico = models.CharField(max_length=255)
    tratamiento = models.TextField()
    sintomas = models.TextField(blank=True, null=True)  
    responsable = models.CharField(max_length=255)

    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-fecha']

    def __str__(self):
        return f"{self.animal.numero_arete} - {self.fecha}"


class Inseminacion(models.Model):
    fecha = models.DateField()
    tipo_semen = models.CharField(max_length=100)
    inseminador = models.CharField(max_length=200)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE)
    responsable = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Servicio {self.animal.numero_arete} - {self.fecha}"


class ConfirmacionGestacion(models.Model):
    fecha_confirmacion = models.DateField()
    metodo_diagnostico = models.CharField(max_length=100)
    resultado = models.CharField(
        max_length=20,
        choices=[
            ('gestante', 'Gestación Confirmada'),
            ('negativa', 'No Gestante')
        ]
    )
    observaciones = models.TextField(null=True, blank=True)
    responsable = models.CharField(max_length=255)

    inseminacion = models.OneToOneField(Inseminacion, on_delete=models.CASCADE)

    def __str__(self):
        return f"Confirmación {self.inseminacion.animal.numero_arete}"
