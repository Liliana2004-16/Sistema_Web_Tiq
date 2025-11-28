# apps/users/decorators.py
from django.core.exceptions import PermissionDenied
from functools import wraps

def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if not user.is_authenticated:
                raise PermissionDenied
            role = getattr(user.rol, 'nombre_rol', None) or getattr(user, 'rol', None)
            if isinstance(role, str):
                role_val = role.lower()
            else:
                role_val = str(role).lower() if role else ''
            allowed = [r.lower() for r in allowed_roles]
            if role_val in allowed:
                return view_func(request, *args, **kwargs)
            raise PermissionDenied
        return _wrapped_view
    return decorator
