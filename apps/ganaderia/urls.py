# apps/ganaderia/urls.py
from django.urls import path
from . import views

app_name = 'ganaderia'

urlpatterns = [
    path('animales/', views.animales_list, name='animales_list'),
    path('animales/<int:pk>/', views.animal_detail, name='animal_detail'),
    path('pesajes/', views.registrar_pesaje_view, name='registrar_pesaje'),  # podrías separar list y create
    path('partos/registrar/', views.registrar_parto_view, name='registrar_parto'),
    path('partos/', views.partos_list, name='partos_list'),
    path("partos/excel/", views.partos_excel, name="partos_excel"),
    path('produccion/', views.registrar_produccion_view, name='registrar_produccion'),
    path('eventos-salida/', views.registrar_evento_salida_view, name='eventos_salida'),
    path('traslados/', views.traslados_view, name='traslados'),
]
