from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone
from django.urls import reverse

from apps.finca.models import Finca
from apps.users.models import User

class AnimalQuerySet(models.QuerySet):
    def activos(self):
        return self.filter(estado='activo')

    def by_arete(self, numero_arete):
        return self.filter(numero_arete__iexact=numero_arete)

class AnimalManager(models.Manager):
    def get_queryset(self):
        return AnimalQuerySet(self.model, using=self._db)

    def get_by_arete(self, numero_arete):
        return self.get_queryset().by_arete(numero_arete).first()

class Animal(models.Model):
    ESTADO_CHOICES = [
        ('activo', 'Activo'),
        ('vendido', 'Vendido'),
        ('muerto', 'Muerto'),
        ('trasladado', 'Trasladado'),
        ('inactivo', 'Inactivo'),
    ]

    id = models.BigAutoField(primary_key=True)
    numero_arete = models.CharField(max_length=50, unique=True)
    nombre = models.CharField(max_length=100, blank=True)
    fecha_nacimiento = models.DateField(null=True, blank=True)
    raza = models.CharField(max_length=100, blank=True)
    sexo = models.CharField(max_length=10, choices=[('M','Macho'), ('F','Hembra')])
    estado = models.CharField(max_length=20, choices=ESTADO_CHOICES, default='activo')
    finca = models.ForeignKey(Finca, on_delete=models.PROTECT, related_name='animales')
    madre = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='crias')
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    objects = AnimalManager()

    class Meta:
        ordering = ['numero_arete']
        verbose_name = 'Animal'
        verbose_name_plural = 'Animales'

    def __str__(self):
        return f"{self.numero_arete} - {self.nombre or 'Sin nombre'}"

    def clean(self):
        if self.madre and self.madre.id == self.id:
            raise ValidationError("Un animal no puede ser su propia madre.")
        if self.sexo not in ('M', 'F'):
            raise ValidationError("Sexo inválido.")
        super().clean()

    @property
    def edad_dias(self):
        if not self.fecha_nacimiento:
            return None
        delta = timezone.now().date() - self.fecha_nacimiento
        return delta.days

    def get_absolute_url(self):
        return reverse('ganaderia:animal_detail', args=[self.pk])

    def latest_pesaje(self):
        return self.pesajes.order_by('-fecha').first()

    def can_register_parto(self):
        return self.sexo == 'F' and self.estado == 'activo'

class Pesaje(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField()
    peso = models.FloatField()
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='pesajes')
    finca = models.ForeignKey(Finca, on_delete=models.PROTECT, related_name='pesajes')  

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Pesaje'
        verbose_name_plural = 'Pesajes'

    def __str__(self):
        return f"{self.animal.numero_arete} - {self.peso}kg - {self.fecha}"

    def clean(self):
        if self.peso <= 0:
            raise ValidationError("El peso debe ser mayor a 0.")
        if self.animal.estado in ['muerto', 'vendido', 'inactivo']:
            raise ValidationError("No se puede registrar pesaje para un animal en estado final.")
        super().clean()

class Parto(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha_nacimiento = models.DateField()
    madre = models.ForeignKey(Animal, on_delete=models.PROTECT, related_name='partos')
    cria = models.ForeignKey(Animal, null=True, blank=True, on_delete=models.SET_NULL, related_name='nacimiento_parto')
    finca = models.ForeignKey(Finca, on_delete=models.PROTECT, related_name='partos')
    peso = models.FloatField(null=True, blank=True)
    raza = models.CharField(max_length=100, blank=True)
    sexo = models.CharField(max_length=10, choices=[('M','Macho'), ('F','Hembra')])

    created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-fecha_nacimiento']
        verbose_name = 'Parto'
        verbose_name_plural = 'Partos'

    def __str__(self):
        return f"Parto: {self.madre.numero_arete} - {self.fecha_nacimiento}"

    def clean(self):
        if self.madre.sexo != 'F':
            raise ValidationError("La madre debe ser hembra.")
        super().clean()

class ProduccionLeche(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField()
    peso_am = models.FloatField(null=True, blank=True)
    peso_pm = models.FloatField(null=True, blank=True)
    animal = models.ForeignKey(Animal, on_delete=models.CASCADE, related_name='producciones')
    finca = models.ForeignKey(Finca, on_delete=models.PROTECT, related_name='producciones')

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Producción de Leche'
        verbose_name_plural = 'Producción de Leche'

    @property
    def total_diario(self):
        return (self.peso_am or 0) + (self.peso_pm or 0)

    def clean(self):

        if not self.animal_id:  
            return

        if self.animal.sexo != 'F':
            raise ValidationError("Solo hembras pueden registrar producción de leche.")

        if (self.peso_am is not None and self.peso_am < 0) or \
            (self.peso_pm is not None and self.peso_pm < 0):
            raise ValidationError("Los valores de peso deben ser >= 0.")

        return super().clean()

class EventoSalida(models.Model):
    TIPO_CHOICES = [('venta', 'Venta'), ('muerte', 'Muerte'), ('descarte','Descarte')]
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateField()
    tipo_evento = models.CharField(max_length=30, choices=TIPO_CHOICES)
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, related_name='eventos_salida')
    responsable = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
    observaciones = models.TextField(blank=True)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Evento de Salida'
        verbose_name_plural = 'Eventos de Salida'

    def clean(self):
        from django.core.exceptions import ValidationError
        if not self.animal_id:
            return
        animal = self.animal
        if animal.estado in ['vendido', 'muerto']:
            raise ValidationError("El animal ya tiene un evento de salida registrado.")

        super().clean()

class Traslado(models.Model):
    id = models.BigAutoField(primary_key=True)
    fecha = models.DateTimeField(auto_now_add=True)
    finca_origen = models.ForeignKey(Finca, on_delete=models.PROTECT, related_name='traslados_origen')
    finca_destino = models.ForeignKey(Finca, on_delete=models.PROTECT, related_name='traslados_destino')
    animal = models.ForeignKey(Animal, on_delete=models.PROTECT, related_name='traslados')
    usuario = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)

    class Meta:
        ordering = ['-fecha']
        verbose_name = 'Traslado'
        verbose_name_plural = 'Traslados'

    def clean(self):
        if self.finca_origen_id == self.finca_destino_id:
            raise ValidationError("La finca destino debe ser diferente a la origen.")
        super().clean()

