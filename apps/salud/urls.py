from django.urls import path
from . import views

app_name = "salud"

urlpatterns = [
    path('eventos/', views.evento_sanitario_list, name="evento_sanitario_list"),
    path('eventos/registrar/', views.evento_sanitario_create, name="evento_sanitario_create"),
    path('eventos/exportar/', views.export_eventos_excel, name="export_eventos_excel"),
    path('eventos/<int:pk>/editar/', views.evento_sanitario_edit, name="evento_sanitario_edit"),
    path('eventos/<int:pk>/eliminar/', views.evento_sanitario_delete, name="evento_sanitario_delete"),
    path('eventos/exportar/', views.export_eventos_excel, name="export_eventos_excel"),
    path('buscar-animal/', views.buscar_animal, name="buscar_animal"),
    path('inseminacion/', views.inseminacion_list, name="inseminacion_list"),
    path('inseminacion/registrar/', views.inseminacion_create, name="inseminacion_create"),
    path('inseminacion/editar/<int:pk>/', views.inseminacion_edit, name="inseminacion_edit"),
    path('inseminacion/eliminar/<int:pk>/', views.inseminacion_delete, name="inseminacion_delete"),
    path('gestacion/pendientes/', views.gestacion_pendientes, name="gestacion_pendientes"),
    path('gestacion/confirmar/<int:id_inseminacion>/', views.confirmar_gestacion, name="confirmar_gestacion"),
    path('gestacion/historial/', views.gestacion_historial, name="gestacion_historial"),


]
