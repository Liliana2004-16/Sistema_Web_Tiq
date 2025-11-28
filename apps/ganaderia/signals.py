# apps/ganaderia/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import EventoSalida, Parto

@receiver(post_save, sender=EventoSalida)
def actualizar_estado_animal_en_evento(sender, instance, created, **kwargs):
    if created:
        animal = instance.animal
        if instance.tipo_evento == 'venta':
            animal.estado = 'vendido'
        elif instance.tipo_evento == 'muerte':
            animal.estado = 'muerto'
        else:
            animal.estado = 'inactivo'
        animal.save(update_fields=['estado'])

@receiver(post_save, sender=Parto)
def post_parto_crear(sender, instance, created, **kwargs):
    if created:
        # la creación de la cría ya se realiza desde el service, pero aquí podrías notificar o actualizar contadores
        pass
