
#  **Agrotiquiza – Sistema de Gestión Ganadera**

Agrotiquiza es un sistema web diseñado para la administración integral de fincas ganaderas. Permite gestionar información del ganado, movimientos entre fincas, partos, inventarios, usuarios y reportes. Está construido con **Django**, siguiendo buenas prácticas, arquitectura modular y una estructura escalable.


## **Características principales**

* Gestión de usuarios y roles
* Control de ganado por finca
* Registro de partos
* Traslados de animales entre fincas
* Dashboard con métricas ganaderas
* Inventarios y control de insumos
* Validaciones robustas en formularios
* Exportación a Excel (openpyxl)
* Autenticación y manejo de sesiones
* Notificaciones con mensajes (toasts)


##  **Arquitectura del Proyecto**

```
Agrotiquiza/
├── README.md                     # Documentación principal del proyecto
├── agrotiquiza_env/              # Entorno virtual 
│
├── agrotiquiza/                  # Configuración principal del proyecto
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── asgi.py
│   ├── wsgi.py
│
├── apps/                         # Aplicaciones del sistema
│   ├── ganaderia/                # Gestión de ganado, partos, traslados
│   ├── inventario/               # Módulo de inventarios
│   ├── usuarios/                 # Autenticación, perfiles, roles
│   ├── salud/                    # Gestion de salud, Eventos sanitarios, inseminaciones
│   ├── finca/                    # Gestion de fincas
│
├── manage.py                     # Comando principal de Django
└── requirements.txt              # Dependencias para instalación
```


## **Tecnologías utilizadas**

| Tecnología       | Descripción                    |
| ---------------- | ------------------------------ |
| **Python 3.10+** | Lenguaje principal             |
| **Django 5.2.8** | Framework backend              |
| **MySQL**        | Base de datos                  |
| **Bootstrap 5**  | Interfaz gráfica               |
| **OpenPyXL**     | Exportación de datos           |
| **DotEnv**       | Manejo de variables de entorno |


## **Requerimientos**

Archivo `requirements.txt`:

```
asgiref==3.10.0
Django==5.2.8
et_xmlfile==2.0.0
mysqlclient==2.2.7
openpyxl==3.1.5
python-dotenv==1.2.1
sqlparse==0.5.3
tzdata==2025.2
```


## **Instalación y configuración**

### 1 Clonar el repositorio

```bash
git clone https://github.com/Liliana2004-16/Sistema_Web_Tiq.git
cd Sistema_Web_Tiq
```

### 2 Crear entorno virtual

```bash
python -m venv agrotiquiza_env
```

### 3 Activar el entorno virtual

Windows:

```bash
agrotiquiza_env\Scripts\activate
```

Linux/Mac:

```bash
source agrotiquiza_env/bin/activate
```

### 4 Instalar dependencias

```bash
pip install -r requirements.txt
```

### 5 Configurar variables de entorno

Crear archivo `.env` en la raíz con:

```
SECRET_KEY=tu_clave
DEBUG=True
DB_NAME=agrotiquiza
DB_USER=root
DB_PASSWORD=tu_password
DB_HOST=localhost
DB_PORT=3306
```

## **Migraciones**

```bash
python manage.py makemigrations
python manage.py migrate
```


##  **Ejecutar el servidor**

```bash
python manage.py runserver
```


##  **Usuarios principales (demo)**

| Rol                   | Usuario     | Contraseña  |
| -------------         | --------    | ----------- |
| Gerente               | 1002683179  | 1234        |
| Adminitrador finca    | 6878989     | Mali432*    |
| Auxiliar Adminitrtiva | auxiliar123 | Cami432*    |



## **Módulos principales**

### Gestión de ganado

* Registro de animales
* Historial de movimientos
* Partos y reproducción
* Estado por finca

### Inventario ganadero

* Alimentos
* Medicamentos
* Lotes de insumos
* Entradas y salidas

### Traslado de ganado

* Selección de animales
* Cambio automático de finca
* Registro histórico
* Validaciones automáticas

### Dashboard (DashWare)

* Cantidad de ganado por finca
* % hembras / machos
* Partos recientes
* Total de fincas
* Estados de producción


## **Seguridad**

* Protección de rutas por roles
* Manejo de sesiones
* Cambios de contraseña temporales
* Validaciones personalizadas


## **Contribución**

1. Haz un fork del proyecto
2. Crea tu rama:

   ```bash
   git checkout -b feature/nueva-funcion
   ```
3. Haz commit con mensajes claros
4. Envía un Pull Request

##  **Licencia**

Proyecto de uso privado para Agrotiquiza S.A.S.
No se permite su distribución sin autorización.


