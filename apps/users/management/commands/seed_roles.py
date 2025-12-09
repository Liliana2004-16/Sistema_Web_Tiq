from django.core.management.base import BaseCommand
from apps.users.models import Rol

class Command(BaseCommand):
    help = 'Llena la tabla de roles con datos iniciales'

    def handle(self, *args, **options):
        roles = [
            'Gerente',
            'Administrador Finca',
            'Auxiliar administrativa',

        ]
        
        for nombre_rol in roles:
            rol, created = Rol.objects.get_or_create(nombre_rol=nombre_rol)
            if created:
                self.stdout.write(
                    self.style.SUCCESS(f'Rol "{nombre_rol}" creado')
                )
            else:
                self.stdout.write(
                    self.style.WARNING(f'Rol "{nombre_rol}" ya existe')
                )
        
        self.stdout.write(
            self.style.SUCCESS(f'\n Total de roles en DB: {Rol.objects.count()}')
        )