#!/usr/bin/env bash
set -o errexit

echo "🚀 ============================================"
echo "🚀 INICIANDO BUILD - $(date)"
echo "🚀 ============================================"

# Instalar dependencias
echo ""
echo "📦 Instalando dependencias..."
pip install -r requirements.txt

# Ejecutar migraciones
echo ""
echo "🔄 Ejecutando migraciones..."
python manage.py migrate

# Crear roles
echo ""
echo "👥 ============================================"
echo "👥 CREANDO ROLES..."
echo "👥 ============================================"
python manage.py seed_roles || echo "⚠️ Error en seed_roles"

# Crear superusuario
echo ""
echo "🔑 ============================================"
echo "🔑 CREANDO SUPERUSUARIO..."
echo "🔑 ============================================"
python manage.py createadmin || echo "⚠️ Error en createadmin"

# Verificar usuarios creados
echo ""
echo "👤 Verificando usuarios en BD..."
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
User = get_user_model()
count = User.objects.count()
print(f"✅ Total de usuarios en BD: {count}")
if count > 0:
    for user in User.objects.all()[:5]:
        print(f"   - {user.username} ({user.email})")
EOF

# Crear finca inicial
echo ""
echo "🏠 ============================================"
echo "🏠 VERIFICANDO/CREANDO FINCAS..."
echo "🏠 ============================================"
python manage.py shell << 'EOF'
from apps.finca.models import Finca

finca_count = Finca.objects.count()
print(f"📊 Fincas existentes: {finca_count}")

if finca_count == 0:
    print("✨ Creando finca inicial...")
    finca = Finca.objects.create(
        nombre="Finca Principal",
        ubicacion="Colombia"
    )
    print(f"✅ Finca creada: {finca.nombre}")
else:
    print("ℹ️  Fincas ya existen:")
    for finca in Finca.objects.all():
        print(f"   - {finca.nombre} ({finca.ubicacion})")
EOF

# Verificar si existe el comando seed_animales
echo ""
echo "🔍 ============================================"
echo "🔍 VERIFICANDO COMANDO seed_animales..."
echo "🔍 ============================================"
python manage.py help seed_animales 2>&1 || echo "⚠️ El comando seed_animales NO existe"

# Listar estructura de management/commands
echo ""
echo "📂 Verificando estructura de archivos..."
python manage.py shell << 'EOF'
import os
from pathlib import Path

base_dir = Path(__file__).resolve().parent.parent
ganaderia_path = base_dir / 'apps' / 'ganaderia'

print(f"📁 Buscando en: {ganaderia_path}")

if ganaderia_path.exists():
    print("✅ Carpeta apps/ganaderia existe")
    
    management_path = ganaderia_path / 'management'
    if management_path.exists():
        print("✅ Carpeta management existe")
        print(f"   Archivos: {list(management_path.glob('*'))}")
        
        commands_path = management_path / 'commands'
        if commands_path.exists():
            print("✅ Carpeta commands existe")
            print(f"   Archivos: {list(commands_path.glob('*'))}")
        else:
            print("❌ Carpeta commands NO existe")
    else:
        print("❌ Carpeta management NO existe")
else:
    print("❌ Carpeta apps/ganaderia NO existe")
EOF

# Crear animales
echo ""
echo "🐄 ============================================"
echo "🐄 CREANDO ANIMALES..."
echo "🐄 ============================================"

# Primero verificar si hay fincas
FINCA_COUNT=$(python manage.py shell -c "from apps.finca.models import Finca; print(Finca.objects.count())" 2>/dev/null || echo "0")

if [ "$FINCA_COUNT" -eq "0" ]; then
    echo "❌ No hay fincas. No se pueden crear animales."
else
    echo "✅ Hay $FINCA_COUNT finca(s) disponible(s)"
    
    # Verificar animales existentes
    ANIMAL_COUNT=$(python manage.py shell -c "from apps.ganaderia.models import Animal; print(Animal.objects.count())" 2>/dev/null || echo "0")
    echo "📊 Animales existentes: $ANIMAL_COUNT"
    
    if [ "$ANIMAL_COUNT" -eq "0" ]; then
        echo "✨ Intentando crear animales..."
        python manage.py seed_animales --cantidad 30 || echo "⚠️ Error ejecutando seed_animales"
        
        # Verificar resultado
        NEW_COUNT=$(python manage.py shell -c "from apps.ganaderia.models import Animal; print(Animal.objects.count())" 2>/dev/null || echo "0")
        echo "📊 Animales después del seed: $NEW_COUNT"
    else
        echo "ℹ️  Ya existen animales. Omitiendo seed."
    fi
fi

# Recolectar archivos estáticos
echo ""
echo "📁 ============================================"
echo "📁 RECOLECTANDO ARCHIVOS ESTÁTICOS..."
echo "📁 ============================================"
python manage.py collectstatic --noinput

# Resumen final
echo ""
echo "📊 ============================================"
echo "📊 RESUMEN FINAL"
echo "📊 ============================================"
python manage.py shell << 'EOF'
from django.contrib.auth import get_user_model
from apps.finca.models import Finca
from apps.ganaderia.models import Animal

User = get_user_model()

print(f"👥 Usuarios: {User.objects.count()}")
print(f"🏠 Fincas: {Finca.objects.count()}")
print(f"🐄 Animales: {Animal.objects.count()}")
EOF

echo ""
echo "✅ ============================================"
echo "✅ BUILD COMPLETADO - $(date)"
echo "✅ ============================================"