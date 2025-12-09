from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .forms import LoginForm, UserRegisterForm, RecoverPasswordForm, CustomPasswordChangeForm
from .models import User, Empresa
from .decorators import role_required
import secrets
import string
import random
from django.http import JsonResponse


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)

        if form.is_valid():
            user = form.get_user()
            login(request, user)

            if user.is_temp_password:
                messages.info(request, "Debe cambiar la contraseña temporal antes de continuar.")
                return redirect('users:change_password')

            return redirect('/inventario/')
    else:
        form = LoginForm()

    return render(request, 'users/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.info(request, "Sesión cerrada correctamente.")
    return redirect('users:login')


def recover_password(request):
    if request.method == "POST":
        form = RecoverPasswordForm(request.POST)
        if form.is_valid():
            cedula = form.cleaned_data["cedula"]

            try:
                user = User.objects.get(cedula=cedula)
            except User.DoesNotExist:
                messages.error(request, "La cédula no está registrada.")
                return redirect("users:recover_password")

            temp_password = ''.join(random.choices(string.ascii_letters + string.digits, k=10))

            user.set_password(temp_password)
            user.is_temp_password = True
            user.save()

            try:
                send_mail(
                    subject="Recuperación de contraseña - Sistema Ganadero",
                    message=f"""
                    Hola {user.first_name},

                    Has solicitado recuperar tu contraseña. 
                    Tu nueva contraseña temporal es:

                        {temp_password}

                    Al iniciar sesión deberás cambiarla obligatoriamente.

                    Saludos,
                    Sistema de Ganadería Agrotiquiza
                    """,
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[user.email],
                    fail_silently=False,
                )
                messages.success(request, "Se ha enviado una nueva contraseña a su correo electrónico.")
            except Exception as e:
                messages.error(request, "Error al enviar el correo. Contacte al administrador.")
                
            return redirect("users:login")
    else:
        form = RecoverPasswordForm()

    return render(request, "users/recover_password.html", {"form": form})


@login_required
def change_password(request):
    if not request.user.is_temp_password:
        messages.info(request, "No necesitas cambiar tu contraseña.")
        return redirect("/inventario/")

    if request.method == "POST":
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            user.is_temp_password = False
            user.save()

            update_session_auth_hash(request, user)

            messages.success(request, "¡Contraseña actualizada correctamente! Ya puedes usar el sistema.")
            return redirect("/inventario/")
    else:
        form = CustomPasswordChangeForm(request.user)

    return render(request, "users/change_password.html", {"form": form})


@login_required
@role_required("Gerente")
def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            
            alphabet = string.ascii_letters + string.digits + "!@#$%^&*"
            temp_password = ''.join(secrets.choice(alphabet) for _ in range(12))
            
            user.set_password(temp_password)
            user.is_temp_password = True
            user.save()
            

            email_sent = False
            subject = 'Cuenta creada - Agrotiquiza'
            message = f"""Hola {user.first_name or user.cedula},

            Se ha creado su cuenta en el Sistema de Ganadería Agrotiquiza.

            Usuario (Cédula): {user.cedula}
            Contraseña temporal: {temp_password}

            Por favor, ingrese al sistema y cambie su contraseña inmediatamente.

            Saludos,
            Equipo Agrotiquiza"""
            
            try:
                send_mail(
                    subject, 
                    message, 
                    settings.DEFAULT_FROM_EMAIL, 
                    [user.email], 
                    fail_silently=False
                )
                email_sent = True
            except Exception as e:
                print(f"Error enviando correo: {e}")
            
            return JsonResponse({
                'success': True,
                'user_data': {
                    'nombre': user.first_name,
                    'apellido': user.last_name,
                    'cedula': user.cedula,
                    'email': user.email,
                    'rol': user.rol.nombre_rol if user.rol else 'Sin rol',
                    'temp_password': temp_password,
                    'email_sent': email_sent
                }
            })
        else:
            return JsonResponse({
                'success': False,
                'errors': form.errors
            })
    else:
        form = UserRegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
@role_required("Gerente")
def users_list_view(request):
    users = User.objects.select_related('empresa', 'rol').all().order_by('cedula')
    
    if request.method == 'POST':
        action = request.POST.get('action')
        user_id = request.POST.get('user_id')
        
        if action and user_id:
            target = get_object_or_404(User, pk=user_id)
            
            if action == 'toggle_active':
                target.is_active = not target.is_active
                target.save()
                messages.success(request, f"Usuario {'activado' if target.is_active else 'desactivado'} correctamente.")
            
            elif action == 'change_role':
                new_role_id = request.POST.get('new_role')
                if new_role_id:
                    from .models import Rol
                    new_role = get_object_or_404(Rol, pk=new_role_id)
                    target.rol = new_role
                    target.save()
                    messages.success(request, f"Rol actualizado a {new_role.nombre_rol}.")
        
        return redirect('users:users_list')
    
    return render(request, 'users/users_list.html', {'users': users})


def dashboard_view(request):
    """Vista del Dashboard - Redirige a inventario"""
    return redirect('/inventario/')