from django.contrib import admin
from .models import Animal, Pesaje, Parto, ProduccionLeche, EventoSalida, Traslado

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    list_display = ('numero_arete', 'nombre', 'sexo', 'raza', 'estado', 'finca')
    search_fields = ('numero_arete', 'nombre')
    list_filter = ('sexo', 'estado', 'finca')

@admin.register(Pesaje)
class PesajeAdmin(admin.ModelAdmin):
    list_display = ('animal', 'peso', 'fecha', 'finca')
    search_fields = ('animal__numero_arete',)

@admin.register(Parto)
class PartoAdmin(admin.ModelAdmin):
    list_display = ('madre', 'fecha_nacimiento', 'cria', 'finca')

@admin.register(ProduccionLeche)
class ProduccionAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'animal', 'peso_am', 'peso_pm', 'total_diario')

@admin.register(EventoSalida)
class EventoSalidaAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'animal', 'tipo_evento', 'responsable')

@admin.register(Traslado)
class TrasladoAdmin(admin.ModelAdmin):
    list_display = ('fecha', 'animal', 'finca_origen', 'finca_destino', 'usuario')
