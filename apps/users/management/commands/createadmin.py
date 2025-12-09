from django.core.management.base import BaseCommand
from apps.users.models import User, Rol, Empresa

class Command(BaseCommand):
    help = 'Crea un superusuario automáticamente si no existe'

    def handle(self, *args, **options):

        cedula = '1234567890'  
        email = 'lilianamartinezdiaz2004@gmail.com'
        password = 'Admin2024!' 
        first_name = 'Liliana'
        last_name = 'Diaz'
  
        if User.objects.filter(cedula=cedula).exists():
            self.stdout.write(
                self.style.WARNING(f'Usuario con cédula "{cedula}" ya existe')
            )
            return
        
        rol_gerente, created = Rol.objects.get_or_create(
            nombre_rol='Gerente'
        )
        if created:
            self.stdout.write(
                self.style.SUCCESS('✅ Rol "Gerente" creado')
            )
        
        # Crear el superusuario
        try:
            user = User.objects.create_superuser(
                cedula=cedula,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                rol=rol_gerente
            )
            
            self.stdout.write(
                self.style.SUCCESS(
                    f'\n'
                    f'═══════════════════════════════════════\n'
                    f' SUPERUSUARIO CREADO EXITOSAMENTE\n'
                    f'═══════════════════════════════════════\n'
                    f'  Cédula:   {cedula}\n'
                    f'  Email:    {email}\n'
                    f'  Password: {password}\n'
                    f'  Nombre:   {first_name} {last_name}\n'
                    f'  Rol:      {rol_gerente.nombre_rol}\n'
                    f'═══════════════════════════════════════\n'
                )
            )
            
        except Exception as e:
            self.stdout.write(
                self.style.ERROR(f' Error al crear superusuario: {str(e)}')
            )