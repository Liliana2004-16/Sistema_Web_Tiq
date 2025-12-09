# apps/ganaderia/management/commands/seed_animales.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import random

from apps.ganaderia.models import Animal
from apps.finca.models import Finca


class Command(BaseCommand):
    help = 'Llena la tabla de animales con datos de ejemplo'

    def add_arguments(self, parser):
        parser.add_argument(
            '--cantidad',
            type=int,
            default=20,
            help='Cantidad de animales a crear (default: 20)'
        )
        parser.add_argument(
            '--limpiar',
            action='store_true',
            help='Elimina todos los animales existentes antes de crear nuevos'
        )

    def handle(self, *args, **options):
        cantidad = options['cantidad']
        limpiar = options['limpiar']

        # Verificar que exista al menos una finca
        fincas = Finca.objects.all()
        if not fincas.exists():
            self.stdout.write(self.style.ERROR('No hay fincas registradas. Crea al menos una finca primero.'))
            return

        # Limpiar animales si se solicita
        if limpiar:
            count = Animal.objects.count()
            Animal.objects.all().delete()
            self.stdout.write(self.style.WARNING(f'🗑️  Se eliminaron {count} animales existentes'))

        # Datos para generar animales
        nombres_machos = [
            'Toro', 'Zeus', 'Thor', 'Rocky', 'Max','Bruno'
        ]
        
        nombres_hembras = [
            'Bella', 'Luna', 'Estrella', 'Paloma', 'Rosa', 'Margarita', 'Dalia',
            'Camila', 'Sofia', 'Valentina', 'Lucero', 'Princesa', 'Reina', 'Dulce'
        ]

        razas = [
            'Holstein', 'Jersey', 'Brahman'
        ]

        estados = ['activo', 'activo', 'activo', 'activo', 'vendido', 'inactivo']  # Más activos

        animales_creados = []
        hembras_creadas = []

        self.stdout.write(self.style.SUCCESS(f'\n Creando {cantidad} animales...\n'))

        for i in range(1, cantidad + 1):
            # Asignar sexo (60% hembras, 40% machos para simular ganado lechero)
            sexo = 'F' if random.random() < 0.6 else 'M'
            
            # Seleccionar nombre según sexo
            if sexo == 'F':
                nombre = random.choice(nombres_hembras)
            else:
                nombre = random.choice(nombres_machos)

            # Generar número de arete único
            numero_arete = f"A{1000 + i}"
            
            # Verificar que no exista
            while Animal.objects.filter(numero_arete=numero_arete).exists():
                numero_arete = f"A{1000 + random.randint(1, 9999)}"

            # Fecha de nacimiento (entre 6 meses y 8 años atrás)
            dias_atras = random.randint(180, 2920)
            fecha_nacimiento = timezone.now().date() - timedelta(days=dias_atras)

            # Asignar finca aleatoria
            finca = random.choice(fincas)

            # Seleccionar raza
            raza = random.choice(razas)

            # Estado (más probabilidad de estar activo)
            estado = random.choice(estados)

            # Asignar madre si es posible (solo si hay hembras creadas)
            madre = None
            if hembras_creadas and random.random() < 0.3:  # 30% tienen madre registrada
                posibles_madres = [h for h in hembras_creadas if h.fecha_nacimiento < fecha_nacimiento]
                if posibles_madres:
                    madre = random.choice(posibles_madres)

            try:
                animal = Animal.objects.create(
                    numero_arete=numero_arete,
                    nombre=f"{nombre} {i}",
                    fecha_nacimiento=fecha_nacimiento,
                    raza=raza,
                    sexo=sexo,
                    estado=estado,
                    finca=finca,
                    madre=madre
                )

                animales_creados.append(animal)
                
                if sexo == 'F':
                    hembras_creadas.append(animal)

                # Mostrar progreso
                sexo_emoji = '' if sexo == 'F' else ''
                self.stdout.write(
                    f'{sexo_emoji} [{i}/{cantidad}] {animal.numero_arete} - {animal.nombre} '
                    f'({animal.raza}, {animal.get_sexo_display()}, {animal.estado})'
                )

            except Exception as e:
                self.stdout.write(self.style.ERROR(f' Error creando animal {i}: {str(e)}'))

        # Resumen final
        self.stdout.write(self.style.SUCCESS(f'\nSe crearon {len(animales_creados)} animales exitosamente'))
        
        # Estadísticas
        total_machos = len([a for a in animales_creados if a.sexo == 'M'])
        total_hembras = len([a for a in animales_creados if a.sexo == 'F'])
        total_activos = len([a for a in animales_creados if a.estado == 'activo'])
        
        self.stdout.write(self.style.SUCCESS(f'\n Estadísticas:'))
        self.stdout.write(f'   • Machos: {total_machos}')
        self.stdout.write(f'   • Hembras: {total_hembras}')
        self.stdout.write(f'   • Activos: {total_activos}')
        self.stdout.write(f'   • Otros estados: {len(animales_creados) - total_activos}')
        self.stdout.write(f'   • Fincas utilizadas: {fincas.count()}\n')