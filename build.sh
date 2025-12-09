set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

python manage.py seed_roles

# Crear superusuario automáticamente
python manage.py createadmin


# Crear animales solo si no existen
python manage.py shell << 'EOF'
from apps.ganaderia.models import Animal

if Animal.objects.count() == 0:
    import subprocess
    print("Creando animales iniciales...")
    subprocess.run(["python", "manage.py", "seed_animales", "--cantidad", "20"])
else:
    print(f"Ya existen {Animal.objects.count()} animales. Omitiendo seed.")
EOF

# Recolectar archivos estáticos
python manage.py collectstatic --noinput

