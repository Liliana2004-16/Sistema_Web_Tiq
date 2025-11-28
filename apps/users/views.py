# apps/users/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, UserRegisterForm, RecoverPasswordForm, ForceChangePasswordForm
from .models import User, Empresa
import secrets
import string

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            cedula = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=cedula, password=password)
            if user is None:
                messages.error(request, "Cédula o contraseña incorrecta")
                return render(request, 'users/login.html', {'form': form})
            if not user.is_active:
                messages.error(request, "Usuario inactivo. Contacte al administrador.")
                return render(request, 'users/login.html', {'form': form})
            login(request, user)
            # Si tiene contraseña temporal, forzar cambio
            if user.is_temp_password:
                messages.info(request, "Debe cambiar la contraseña temporal recibida.")
                return redirect('users:change_password')
            # redirigir según rol (ajusta rutas si necesitas otras páginas)
            return redirect('users:dashboard')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('users:login')

@login_required
def dashboard_view(request):
    return render(request, 'dashboard.html')

# Recuperar contraseña (HU02)
def recover_password_view(request):
    if request.method == 'POST':
        form = RecoverPasswordForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data['cedula']
            user = User.objects.get(cedula=cedula)
            # generar contraseña temporal segura
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_"
            temp_password = ''.join(secrets.choice(alphabet) for _ in range(10))
            user.set_password(temp_password)
            user.is_temp_password = True
            user.save()
            # Enviar correo (requiere configuración en settings)
            subject = 'Recuperación de contraseña - Agrotiquiza'
            message = f'Hola {user.first_name or user.cedula},\n\nSe ha generado una contraseña temporal: {temp_password}\nPor seguridad deberá cambiarla al ingresar.\n\nSi usted no solicitó esto, contacte al administrador.'
            from_email = settings.DEFAULT_FROM_EMAIL
            recipient = [user.email]
            try:
                send_mail(subject, message, from_email, recipient, fail_silently=False)
                messages.success(request, "Se ha enviado una nueva contraseña a su correo electrónico")
                return redirect('users:login')
            except Exception as e:
                # En entornos de desarrollo, fallback: mostrar la pwd en consola/ mensajes
                messages.warning(request, f"No fue posible enviar correo. Contraseña temporal: {temp_password}")
                return redirect('users:login')
    else:
        form = RecoverPasswordForm()
    return render(request, 'users/recover_password.html', {'form': form})

@login_required
def change_password_view(request):
    user = request.user
    if request.method == 'POST':
        form = ForceChangePasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            # limpiamos flag y mantenemos sesión
            user.is_temp_password = False
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Contraseña actualizada correctamente.")
            return redirect('users:dashboard')
    else:
        form = ForceChangePasswordForm(user)
    return render(request, 'users/change_password.html', {'form': form})

# helper: solo Gerente
def is_gerente(u):
    return u.is_authenticated and (u.rol == 'Gerente' or u.is_superuser)

# Registro de usuario HU04 - solo Gerente
@login_required
@user_passes_test(is_gerente)
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
                messages.success(request, f"Usuario creado correctamente. Contraseña temporal: {temp_password}")
            return redirect('users:users_list')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})

# Gestión de usuarios HU05 - listado, activar/desactivar, editar (solo Gerente)
@login_required
@user_passes_test(is_gerente)
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

