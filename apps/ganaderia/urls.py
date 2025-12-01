# apps/ganaderia/urls.py
from django.urls import path
from . import views

app_name = 'ganaderia'

urlpatterns = [
    path('animales/', views.animales_list, name='animales_list'),
    path('animales/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('pesajes/', views.pesajes_list_view, name='pesajes_list'),
    path('ajax/buscar-animal/', views.buscar_animal_por_arete, name='buscar_animal'),
    path('pesajes/<int:pk>/editar/', views.pesaje_edit_view, name='pesaje_edit'),
    path('pesajes/<int:pk>/eliminar/', views.pesaje_delete_view, name='pesaje_delete'),
    path('partos/registrar/', views.registrar_parto_view, name='registrar_parto'),
    path('partos/', views.partos_list, name='partos_list'),
    path('partos/<int:id>/editar/', views.editar_parto, name='editar_parto'),
    path('partos/<int:id>/eliminar/', views.eliminar_parto, name='eliminar_parto'),
    path("partos/excel/", views.partos_excel, name="partos_excel"),
    path('produccion/', views.registrar_produccion_view, name='registrar_produccion'),
    
    path('produccion/am/', views.produccion_am_view, name="produccion_am"),
    path('produccion/pm/', views.produccion_pm_view, name="produccion_pm"),
    path('produccion/exportar/', views.produccion_export_excel, name="produccion_exportar"),
    path('produccion/detalle/', views.registrar_produccion_view, name="produccion_detalle"),

    path('eventos-salida/', views.registrar_evento_salida_view, name='eventos_salida'),
    path('traslados/', views.traslados_view, name='traslados'),
]
