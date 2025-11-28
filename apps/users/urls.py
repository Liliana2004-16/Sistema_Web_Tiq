# apps/users/urls.py
from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    path('register/', views.register_view, name='register'),               # acceso Gerente
    path('users/', views.users_list_view, name='users_list'),              # gestión de usuarios (Gerente)
    path('recover-password/', views.recover_password_view, name='recover_password'),
    path('change-password/', views.change_password_view, name='change_password'),
]

