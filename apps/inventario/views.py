# apps/inventario/views.py

from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count, Avg, F, Q, Sum, ExpressionWrapper,  FloatField

from apps.ganaderia.models import Animal, EventoSalida, Parto, ProduccionLeche, Traslado
from apps.salud.models import EventoSanitario, Inseminacion, ConfirmacionGestacion
from apps.finca.models import Finca

@method_decorator(login_required, name='dispatch')
class DashboardView(View):

    def get(self, request):

        # -------------------------------------------------
        # 1. Estados del Ganado
        # -------------------------------------------------
        ventas = EventoSalida.objects.filter(tipo_evento="venta").count()
        muertes = EventoSalida.objects.filter(tipo_evento="muerte").count()
        descartes = EventoSalida.objects.filter(tipo_evento="descarte").count()

        traslados = Traslado.objects.count()

        # Gestantes correctas según tu modelo:
        gestantes = ConfirmacionGestacion.objects.filter(resultado="gestante").count()

        # Vacas activas según Animal:
        vacas_produccion = Animal.objects.filter(estado="activo", sexo="F").count()

        # -------------------------------------------------
        # 2. Ganado por Finca
        # -------------------------------------------------
        ganado_por_finca = (
            Animal.objects.values("finca__nombre")
            .annotate(total=Count("id"))
            .order_by("finca__nombre")
        )

        # -------------------------------------------------
        # 3. Fincas registradas
        # -------------------------------------------------
        total_fincas = Finca.objects.count()

        # -------------------------------------------------
        # 4. Partos
        # -------------------------------------------------
        total_partos = Parto.objects.count()

        # -------------------------------------------------
        # 5. Producción de leche
        # -------------------------------------------------
        # Cambia esta línea:
# Cambia esta línea:
        produccion_por_finca = (
            ProduccionLeche.objects.values(nombre=F("finca__nombre"))
            .annotate(
                promedio=Avg(
                    ExpressionWrapper(
                        (F("peso_am") + F("peso_pm")),
                        output_field=FloatField()
                    )
                )
            )
        )

    # Agregar esto 
        total_animales = Animal.objects.count()

        produccion_diaria = ProduccionLeche.objects.aggregate(
            total=Sum(F("peso_am") + F("peso_pm"))
        )["total"] or 0

        # -------------------------------------------------
        # 6. Eventos sanitarios
        # -------------------------------------------------
        eventos_salud_total = EventoSanitario.objects.count()

        eventos_salud_por_finca = (
            EventoSanitario.objects
            .values("animal__finca__nombre")
            .annotate(total=Count("id"))
        )

        # -------------------------------------------------
        # 7. Inseminaciones
        # -------------------------------------------------
        total_inseminaciones = Inseminacion.objects.count()
        pendientes_confirmar = Inseminacion.objects.filter(confirmaciongestacion__isnull=True).count()

        context = {
            # === ESTADO DEL GANADO ===
            "ventas": ventas,
            "muertes": muertes,
            "descarte": descartes,           # corregido nombre
            "descartes": descartes,          # por si el template usa ambos
            "traslados": traslados,
            "gestantes": gestantes,
            "vacas_produccion": vacas_produccion,

            # === GANADO POR FINCA ===
            "ganado_por_finca": ganado_por_finca,

            # === FINCAS / PARTOS ===
            "total_fincas": total_fincas,
            "total_partos": total_partos,

            # === PRODUCCIÓN ===
            "produccion_por_finca": produccion_por_finca,

            # === SALUD ===
            "eventos_salud_total": eventos_salud_total,
            "eventos_salud_por_finca": eventos_salud_por_finca,

            # === INSEMINACIONES ===
            "total_inseminaciones": total_inseminaciones,
            "pendientes_confirmar": pendientes_confirmar,
        }

        return render(request, "dashboard.html", context)
