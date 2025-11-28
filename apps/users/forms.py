# apps/users/forms.py

from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, SetPasswordForm
from .models import User, Empresa
from django.core.exceptions import ValidationError
import re


# ============================================================
# LOGIN
# ============================================================
class LoginForm(AuthenticationForm):
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
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Contraseña'}),
    )

    def clean_username(self):
        ced = self.cleaned_data.get('username')
        if not ced or not re.fullmatch(r'\d+', ced):
            raise ValidationError('La cédula debe contener solo números.')
        return ced


# ============================================================
# REGISTRO DE USUARIOS
# ============================================================
class UserRegisterForm(UserCreationForm):

    empresa = forms.ModelChoiceField(
        queryset=Empresa.objects.all(),
        required=False,
        label="Empresa"
    )

    # Sobrescribimos los campos de contraseña para traducirlos
    password1 = forms.CharField(
        label="Contraseña",
        widget=forms.PasswordInput,
        help_text="Debe contener al menos 8 caracteres y no ser demasiado común."
    )
    password2 = forms.CharField(
        label="Confirmar contraseña",
        widget=forms.PasswordInput,
        help_text="Repita la contraseña para verificación."
    )

    class Meta:
        model = User
        fields = ('cedula', 'first_name', 'last_name', 'email', 'rol', 'empresa')

        labels = {
            'cedula': 'Cédula',
            'first_name': 'Nombre',
            'last_name': 'Apellido',
            'email': 'Correo electrónico',
            'rol': 'Rol',
            'empresa': 'Empresa',
        }

        widgets = {
            'cedula': forms.TextInput(attrs={'pattern': '[0-9]+'}),
        }

    # Validación de cédula
    def clean_cedula(self):
        ced = self.cleaned_data.get('cedula')
        if not ced or not ced.isdigit():
            raise ValidationError("La cédula solo debe contener números.")
        return ced

    # Validación de correo
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError("El correo ya está registrado.")
        return email

    # Validación general
    def clean(self):
        cleaned = super().clean()
        ced = cleaned.get('cedula')

        if ced and User.objects.filter(cedula=ced).exists():
            raise ValidationError("La cédula ya está registrada.")

        return cleaned


# ============================================================
# RECUPERACIÓN DE CONTRASEÑA
# ============================================================
class RecoverPasswordForm(forms.Form):
    cedula = forms.CharField(
        label='Cédula',
        max_length=20,
        widget=forms.TextInput(attrs={'pattern': '[0-9]+', 'inputmode': 'numeric'})
    )

    def clean_cedula(self):
        ced = self.cleaned_data.get('cedula')
        if not ced.isdigit():
            raise ValidationError('La cédula debe contener solo números.')
        if not User.objects.filter(cedula=ced).exists():
            raise ValidationError('No existe un usuario con esa cédula.')
        return ced


# ============================================================
# CAMBIO OBLIGATORIO DE CONTRASEÑA
# ============================================================
class ForceChangePasswordForm(SetPasswordForm):
    pass
