# apps/salud/services.py

from django.db import transaction
from django.core.exceptions import ValidationError

from apps.ganaderia.models import Animal
from apps.users.models import User
from .models import (
    EventoSanitario,
    Inseminacion,
    ConfirmacionGestacion
)


class EventoSanitarioService:

    @staticmethod
    @transaction.atomic
    def registrar_evento_sanitario(
        fecha, animal, diagnostico, tratamiento,
        responsable, sintomas=None
    ):
        """
        Crea un evento sanitario validando animal existente
        y asegurando consistencia en una transacción.
        """

        if not Animal.objects.filter(id=animal.id).exists():
            raise ValidationError("El animal no existe.")

        evento = EventoSanitario.objects.create(
            fecha=fecha,
            animal=animal,
            diagnostico=diagnostico,
            tratamiento=tratamiento,
            responsable=responsable,
            sintomas=sintomas,
        )

        return evento


class InseminacionService:

    @staticmethod
    @transaction.atomic
    def registrar_inseminacion(
        fecha, animal, tipo_semen, inseminador, usuario_responsable
    ):

        if animal.estado == "Gestante":
            raise ValidationError("No se puede inseminar un animal gestante.")

        return Inseminacion.objects.create(
            fecha=fecha,
            animal=animal,
            tipo_semen=tipo_semen,
            inseminador=inseminador,
            responsable=usuario_responsable
        )


class GestacionService:

    @staticmethod
    def obtener_inseminaciones_pendientes():
        """
        Devuelve todas las inseminaciones sin confirmación.
        """
        return Inseminacion.objects.filter(confirmaciongestacion__isnull=True)

    @staticmethod
    @transaction.atomic
    def confirmar_gestacion(
        inseminacion, fecha_confirmacion,
        metodo_diagnostico, resultado,
        responsable, observaciones=None
    ):
        """
        Registra la confirmación de gestación y actualiza estado del animal.
        """

        # Verificar que no exista ya una confirmación
        if hasattr(inseminacion, "confirmaciongestacion"):
            raise ValidationError("Esta inseminación ya fue confirmada.")

        confirm = ConfirmacionGestacion.objects.create(
            inseminacion=inseminacion,
            fecha_confirmacion=fecha_confirmacion,
            metodo_diagnostico=metodo_diagnostico,
            resultado=resultado,
            responsable=responsable,
            observaciones=observaciones
        )

        # Actualización del estado del animal
        animal = inseminacion.animal
        animal.estado = "Gestante" if resultado == "gestante" else "No gestante"
        animal.save()

        return confirm
