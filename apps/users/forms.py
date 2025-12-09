# apps/users/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm
from .models import User, Empresa, Rol
from django.core.exceptions import ValidationError
import re


# ============================================================
# LOGIN
# ============================================================
class LoginForm(AuthenticationForm):
    error_messages = {
        'invalid_login': "Cédula o contraseña incorrecta.",
        'inactive': "Usuario inactivo. Contacte al administrador.",
    }

    username = forms.CharField(
        label="Cédula",
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ingrese su cédula',
            'pattern': '[0-9]+',
            'inputmode': 'numeric'
        }),
        max_length=20
    )

    password = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Contraseña'
        }),
    )

    def clean_username(self):
        ced = self.cleaned_data.get('username')
        if not ced or not re.fullmatch(r'\d+', ced):
            raise ValidationError('La cédula debe contener solo números.')
        return ced

    def confirm_login_allowed(self, user):
        if not user.is_active:
            raise ValidationError(
                self.error_messages['inactive'],
                code='inactive',
            )


# ============================================================
# REGISTRO DE USUARIOS
# ============================================================
class UserRegisterForm(forms.ModelForm):
    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=False,
        label="Empresa",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    rol = forms.ModelChoiceField(
        queryset=Rol.objects.all(),
        required=True,
        label="Rol",
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    class Meta:
        model = User
        fields = ('cedula', 'first_name', 'last_name', 'email', 'rol', 'empresa')

        labels = {
            'cedula': 'Cédula',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
        }

        widgets = {
            'cedula': forms.TextInput(attrs={
                'class': 'form-control',
                'pattern': '[0-9]+',
                'placeholder': 'Ingrese la cédula'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el nombre'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ingrese el apellido'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'correo@ejemplo.com'
            }),
        }

    def clean_cedula(self):
        ced = self.cleaned_data.get('cedula')
        if not ced or not ced.isdigit():
            raise ValidationError("La cédula solo debe contener números.")
        if User.objects.filter(cedula=ced).exists():
            raise ValidationError("La cédula ya está registrada.")
        return ced

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo ya está registrado.")
        return email


# ============================================================
# RECUPERAR CONTRASEÑA
# ============================================================
class RecoverPasswordForm(forms.Form):
    cedula = forms.CharField(
        label='Cédula',
        max_length=20,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'pattern': '[0-9]+', 
            'inputmode': 'numeric',
            'placeholder': 'Ingrese su cédula'
        })
    )

    def clean_cedula(self):
        ced = self.cleaned_data.get('cedula')
        if not ced.isdigit():
            raise ValidationError('La cédula debe contener solo números.')
        if not User.objects.filter(cedula=ced).exists():
            raise ValidationError('No existe un usuario con esa cédula.')
        return ced


# ============================================================
# CAMBIAR CONTRASEÑA
# ============================================================
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['old_password'].label = "Contraseña actual"
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingrese su contraseña actual'
        })
        
        self.fields['new_password1'].label = "Nueva contraseña"
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Ingrese la nueva contraseña'
        })
        
        self.fields['new_password2'].label = "Confirmar nueva contraseña"
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirme la nueva contraseña'
        })

        self.fields['new_password1'].help_text = (
            "<ul>"
            "<li>La contraseña no puede ser similar a su información personal.</li>"
            "<li>Debe contener al menos 8 caracteres.</li>"
            "<li>No debe ser una contraseña común.</li>"
            "<li>No puede ser completamente numérica.</li>"
            "</ul>"
        )