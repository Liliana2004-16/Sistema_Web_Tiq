# apps/users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.forms import PasswordChangeForm
from .decorators import role_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, UserRegisterForm, RecoverPasswordForm, CustomPasswordChangeForm
from .models import User, Empresa
import secrets
import string
import random


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            # Verificar si debe cambiar contraseña temporal
            if user.is_temp_password:
                messages.info(request, "Debe cambiar la contraseña temporal recibida.")
                return redirect('users:change_password')

            return redirect('/inventario/')
        # Si no es válido, los errores ya están en form.non_field_errors()
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})
def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('users:login')

# Recuperar contraseña (HU02)
def recover_password(request):
    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            cedula = form.cleaned_data["cedula"]

            # Validar usuario
            try:
                user = User.objects.get(cedula=cedula)
            except User.DoesNotExist:
                messages.error(request, "La cédula no está registrada.")
                return redirect("users:recover_password")

            # Generar contraseña temporal
            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            # Guardar contraseña temporal
            user.set_password(temp_password)
            user.is_temp_password = True
            user.save()

            # Enviar correo
            send_mail(
                subject="Recuperación de contraseña - Sistema Ganadero",
                message=f"""
Hola {user.first_name},

Has solicitado recuperar tu contraseña. 
Tu nueva contraseña temporal es:

    {temp_password}

Al iniciar sesión deberás cambiarla obligatoriamente.

Saludos.
""",
                from_email=None,  # toma EMAIL_HOST_USER
                recipient_list=[user.email],
            )

            messages.success(request, "Se ha enviado una nueva contraseña a su correo electrónico.")
            return redirect("users:login")
    else:
        form = RecoverPasswordForm()

    return render(request, "users/recover_password.html", {"form": form})

@login_required
def change_password(request):
    if request.user.is_temp_password is False:
        return redirect("/inventario/")  # no debe estar aquí

    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.is_temp_password = False
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, "La contraseña ha sido actualizada.")
            return redirect("/inventario/")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "users/change_password.html", {"form": form})

# Registro de usuario HU04 - solo Gerente
@login_required
@role_required("Gerente")
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # no se establece contraseña aquí, se crea contraseña temporal y se envía evento si deseas
            user = form.save(commit=False)
            # generar contraseña temporal para nuevo usuario y marcar is_temp_password=True
            import secrets, string
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_"
            temp_password = ''.join(secrets.choice(alphabet) for _ in range(10))
            user.set_password(temp_password)
            user.is_temp_password = True
            user.save()
            # intentar enviar correo con contraseña temporal
            subject = 'Cuenta creada - Agrotiquiza'
            message = f'Hola {user.first_name or user.cedula},\n\nSe ha creado su usuario. Contraseña temporal: {temp_password}\nPor favor ingrese y cambie su contraseña.'
            try:
                send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email], fail_silently=False)
                messages.success(request, "Usuario creado correctamente y contraseña enviada por correo.")
            except Exception:
                messages.warning(
                    request,
                    "Usuario creado correctamente, pero no se pudo enviar el correo. "
                    "Contacte al administrador para recibir su contraseña temporal."
                )
            return redirect('users:users_list')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Gestión de usuarios HU05 - listado, activar/desactivar, editar (solo Gerente)
@login_required
@role_required("Gerente")
def users_list_view(request):
    users = User.objects.select_related('empresa').all().order_by('cedula')
    if request.method == 'POST':
        # ejemplo: activar/desactivar
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        if action and user_id:
            target = get_object_or_404(User, pk=user_id)
            if action == 'toggle_active':
                target.is_active = not target.is_active
                target.save()
                messages.success(request, "Estado actualizado.")
            elif action == 'promote':
                # ejemplo simple para cambiar rol; implementar según necesidad
                new_role = request.POST.get('new_role')
                if new_role in dict(User.ROLES):
                    target.rol = new_role
                    target.save()
                    messages.success(request, "Rol actualizado.")
        return redirect('users:users_list')
    return render(request, 'users/users_list.html', {'users': users})

def dashboard_view(request):
    """Vista del Dashboard - Redirige a inventario"""
    return redirect('/inventario/')

