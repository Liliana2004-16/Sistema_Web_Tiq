# apps/users/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from .models import User, Empresa
from django.utils.translation import gettext_lazy as _

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nombre',)
    search_fields = ('nombre',)

@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('cedula', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'rol', 'empresa')}),
        (_('Flags'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_temp_password')}),
        (_('Permissions'), {'fields': ('groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('cedula', 'email', 'first_name', 'last_name', 'rol', 'empresa', 'password1', 'password2'),
        }),
    )
    list_display = ('cedula', 'email', 'first_name', 'last_name', 'rol', 'is_active', 'is_staff')
    search_fields = ('cedula', 'first_name', 'last_name', 'email')
    ordering = ('cedula',)
