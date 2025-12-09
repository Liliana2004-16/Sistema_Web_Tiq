from django.shortcuts import render
from django.views import View
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.db.models import Count, Avg, F, Q, Sum, ExpressionWrapper, FloatField

from apps.ganaderia.models import Animal, EventoSalida, Parto, ProduccionLeche, Traslado
from apps.salud.models import EventoSanitario, Inseminacion, ConfirmacionGestacion
from apps.finca.models import Finca

@method_decorator(login_required, name='dispatch')
class DashboardView(View):

    def get(self, request):

        ventas = EventoSalida.objects.filter(tipo_evento="venta").count()
        muertes = EventoSalida.objects.filter(tipo_evento="muerte").count()
        descartes = EventoSalida.objects.filter(tipo_evento="descarte").count()
        traslados = Traslado.objects.count()
        gestantes = ConfirmacionGestacion.objects.filter(resultado="gestante").count()
        vacas_produccion = Animal.objects.filter(estado="activo", sexo="F").count()
        ganado_por_finca = (
            Animal.objects.values("finca__nombre")
            .annotate(total=Count("id"))
            .order_by("finca__nombre")
        )

        total_fincas = Finca.objects.count()
        total_partos = Parto.objects.count()

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

        total_animales = Animal.objects.filter(
            Q(estado="activo") | Q(estado="trasladado") | Q(estado="gestante")
        ).count()

        produccion_diaria = ProduccionLeche.objects.aggregate(
            total=Sum(F("peso_am") + F("peso_pm"))
        )["total"] or 0

        eventos_salud_total = EventoSanitario.objects.count()

        eventos_salud_por_finca = (
            EventoSanitario.objects
            .values("animal__finca__nombre")
            .annotate(total=Count("id"))
        )

        total_inseminaciones = Inseminacion.objects.count()
        pendientes_confirmar = Inseminacion.objects.filter(confirmaciongestacion__isnull=True).count()

        context = {
            "ventas": ventas,
            "muertes": muertes,
            "descarte": descartes,
            "descartes": descartes,
            "traslados": traslados,
            "gestantes": gestantes,
            "vacas_produccion": vacas_produccion,
            "ganado_por_finca": ganado_por_finca,
            "total_animales": total_animales,
            "total_fincas": total_fincas,
            "total_partos": total_partos,
            "produccion_por_finca": produccion_por_finca,
            "produccion_diaria": produccion_diaria,
            "eventos_salud_total": eventos_salud_total,
            "eventos_salud_por_finca": eventos_salud_por_finca,
            "total_inseminaciones": total_inseminaciones,
            "pendientes_confirmar": pendientes_confirmar,
        }

        return render(request, "dashboard.html", context)