from django.urls import path
from . import views

app_name = "finca"

urlpatterns = [
    path('', views.finca_list, name='list'),
    path('crear/', views.finca_create, name='create'),
    path('editar/<int:id>/', views.finca_update, name='update'),
    path('eliminar/<int:id>/', views.finca_delete, name='delete'),
]
