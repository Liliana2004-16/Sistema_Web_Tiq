set -o errexit

# Instalar dependencias
pip install -r requirements.txt

# Ejecutar migraciones
python manage.py migrate

# Crear superusuario automáticamente
python manage.py createadmin

# Recolectar archivos estáticos
python manage.py collectstatic --noinput