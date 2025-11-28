# apps/ganaderia/services.py
from django.db import transaction
from django.core.exceptions import ValidationError
from .models import Animal, Pesaje, Parto, ProduccionLeche, EventoSalida, Traslado

class AnimalService:
    @staticmethod
    def get_by_arete(numero_arete):
        return Animal.objects.get_by_arete(numero_arete)

    @staticmethod
    @transaction.atomic
    def registrar_pesaje(numero_arete, fecha, peso, finca, usuario=None):
        animal = Animal.objects.get_by_arete(numero_arete)
        if not animal:
            raise ValidationError("El número de arete no corresponde a ningún animal registrado")
        pesaje = Pesaje(animal=animal, fecha=fecha, peso=peso, finca=finca)
        pesaje.full_clean()
        pesaje.save()
        return pesaje

    @staticmethod
    @transaction.atomic
    def registrar_parto(fecha_nac, numero_arete_madre, numero_arete_cria,
                        nombre_cria, finca, raza, sexo, peso, usuario):

        madre = Animal.objects.get(numero_arete=numero_arete_madre)

        if madre.sexo != "F":
            raise Exception("El animal seleccionado no puede ser madre porque no es hembra.")

        if not madre.can_register_parto():
            raise Exception("No se puede registrar parto para esta hembra.")

        # validar arete duplicado
        if Animal.objects.filter(numero_arete=numero_arete_cria).exists():
            raise Exception("Ya existe un animal registrado con ese número de arete.")

        # Crear la cría
        cria = Animal.objects.create(
            numero_arete=numero_arete_cria,
            nombre=nombre_cria,
            fecha_nacimiento=fecha_nac,
            sexo=sexo,
            raza=raza,
            estado="activo",
            madre=madre,
            finca=finca
        )

        # Registrar el parto
        parto = Parto.objects.create(
            fecha_nacimiento=fecha_nac,
            madre=madre,
            cria=cria,
            finca=finca,
            peso=peso,
            raza=raza,
            sexo=sexo,
            created_by=usuario
        )

        return parto

    @staticmethod
    @transaction.atomic
    def registrar_produccion(numero_arete, fecha, peso_am=None, peso_pm=None, usuario=None):
        animal = Animal.objects.get_by_arete(numero_arete)
        if not animal:
            raise ValidationError("El número de arete no corresponde a ningún animal registrado")
        prod = ProduccionLeche(animal=animal, fecha=fecha, peso_am=peso_am, peso_pm=peso_pm, finca=animal.finca)
        prod.full_clean()
        prod.save()
        return prod

    @staticmethod
    @transaction.atomic
    def registrar_evento_salida(numero_arete, fecha, tipo_evento, usuario=None, observaciones=""):
        animal = Animal.objects.get_by_arete(numero_arete)
        if not animal:
            raise ValidationError("El número de arete no corresponde a ningún animal registrado")
        evento = EventoSalida(animal=animal, fecha=fecha, tipo_evento=tipo_evento, responsable=usuario, observaciones=observaciones)
        evento.full_clean()
        evento.save()
        # actualizar estado del animal
        if tipo_evento == 'venta':
            animal.estado = 'vendido'
        elif tipo_evento == 'muerte':
            animal.estado = 'muerto'
        else:
            animal.estado = 'inactivo'
        animal.save(update_fields=['estado'])
        return evento

    @staticmethod
    @transaction.atomic
    def trasladar_animales(lista_aretes, finca_destino, usuario=None):
        traslados = []
        for arete in lista_aretes:
            animal = Animal.objects.get_by_arete(arete)
            if not animal:
                raise ValidationError(f"No existe el animal con arete {arete}")
            if animal.finca_id == finca_destino.id:
                raise ValidationError(f"El animal {arete} ya está en la finca seleccionada")
            traslado = Traslado(finca_origen=animal.finca, finca_destino=finca_destino, animal=animal, usuario=usuario)
            traslado.full_clean()
            traslado.save()
            # actualizar animal
            animal.finca = finca_destino
            animal.estado = 'trasladado'
            animal.save(update_fields=['finca', 'estado'])
            traslados.append(traslado)
        return traslados
