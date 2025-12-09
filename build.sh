#!/usr/bin/env bash
set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear roles
python manage.py seed_roles

# Crear superusuario automáticamente
python manage.py createadmin

# Crear finca inicial si no existe
python manage.py shell << 'EOF'
from apps.finca.models import Finca

if Finca.objects.count() == 0:
    print(" Creando finca inicial...")
    Finca.objects.create(
        nombre="Finca Principal",
        ubicacion="Colombia"
    )
    print("Finca creada exitosamente")
else:
    print(f"ℹ  Ya existen {Finca.objects.count()} finca(s)")
EOF

# Crear animales solo si no existen
python manage.py shell << 'EOF'
from apps.ganaderia.models import Animal
from apps.finca.models import Finca

if Finca.objects.count() == 0:
    print(" No hay fincas. No se pueden crear animales.")
elif Animal.objects.count() == 0:
    import subprocess
    print(" Creando animales iniciales...")
    result = subprocess.run(["python", "manage.py", "seed_animales", "--cantidad", "30"])
    if result.returncode == 0:
        print(" Animales creados exitosamente")
    else:
        print(" Hubo un problema creando los animales")
else:
    print(f" Ya existen {Animal.objects.count()} animales. Omitiendo seed.")
EOF

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

echo " Build completado exitosamente"