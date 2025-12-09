set -o errexit

echo " Iniciando build..."

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar migraciones
echo "Ejecutando migraciones..."
python manage.py migrate

# Crear roles
echo "Creando roles..."
python manage.py seed_roles

# Crear superusuario automáticamente
echo "Creando superusuario..."
python manage.py createadmin

# Crear finca inicial si no existe
echo "Verificando fincas..."
python manage.py shell << 'EOF'
from apps.finca.models import Finca

if Finca.objects.count() == 0:
    print(" Creando finca inicial...")
    Finca.objects.create(
        nombre="Finca Principal",
        ubicacion="Colombia"
    )
    print(" Finca creada exitosamente")
else:
    print(f"ℹ Ya existen {Finca.objects.count()} finca(s)")
EOF

# Verificar cantidad de animales y crear si es necesario
echo "🐄 Verificando animales..."
ANIMAL_COUNT=$(python manage.py shell -c "from apps.ganaderia.models import Animal; print(Animal.objects.count())")

if [ "$ANIMAL_COUNT" -eq "0" ]; then
    echo "✨ Creando animales iniciales..."
    python manage.py seed_animales --cantidad 30
    echo " Animales creados exitosamente"
else
    echo " Ya existen $ANIMAL_COUNT animales. Omitiendo seed."
fi

# Recolectar archivos estáticos
echo " Recolectando archivos estáticos..."
python manage.py collectstatic --noinput

echo " Build completado exitosamente"