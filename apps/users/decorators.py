from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def role_required(*roles_permitidos):
    """
    Decorador para restringir vistas por rol.
    Uso:
        @role_required("Gerente", "Administrador Finca", )
    """
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):

            if not request.user.is_authenticated:
                messages.error(request, "Debes iniciar sesión.")
                return redirect('users:login')

            if not hasattr(request.user, 'rol') or not request.user.rol:
                messages.error(request, "Tu usuario no tiene un rol asignado.")
                return redirect('users:dashboard')

            rol_usuario = request.user.rol.nombre_rol

            if rol_usuario not in roles_permitidos:
                messages.error(request, "No tienes permisos para acceder a esta sección.")
                return redirect('users:dashboard')

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator
