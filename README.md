# TiendasGeo - Aplicación de Búsqueda de Productos Cercanos

## Descripción del Proyecto

TiendasGeo es una aplicación web que permite a los usuarios buscar productos y encontrar la tienda más cercana donde están disponibles. La aplicación utiliza MongoDB como base de datos NoSQL con capacidades geoespaciales para almacenar la información de tiendas y productos.

## Características Principales

- **Búsqueda geoespacial**: Encuentra la tienda más cercana con el producto que necesitas
- **Carga de inventario por CSV**: Los dueños de tiendas pueden cargar su inventario desde archivos CSV
- **Mapas interactivos**: Visualiza las tiendas en un mapa interactivo
- **Gestión de tiendas**: Interfaz completa para administrar tiendas y productos
- **Autenticación de usuarios**: Sistema de registro e inicio de sesión

## Tecnologías Utilizadas

- **Backend**: Flask + PyMongo
- **Base de datos**: MongoDB (con índices geoespaciales)
- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5
- **Mapas**: Leaflet.js
- **Contenedorización**: Docker y Docker Compose

## Requisitos

- Python 3.10 o superior
- MongoDB 4.4 o superior
- Docker y Docker Compose (opcional, para despliegue)

## Instalación y Ejecución

### Opción 1: Ejecución Local

1. Clona el repositorio:
   ```
   git clone https://github.com/tu-usuario/tiendasgeo.git
   cd tiendasgeo
   ```

2. Crea un entorno virtual e instala las dependencias:
   ```
   python -m venv venv
   source venv/bin/activate  # En Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Asegúrate de tener MongoDB en ejecución en localhost:27017 o configura la variable de entorno `MONGODB_URI` en el archivo `.env`.

5. Pobla la base de datos:
   ```
   python seed_db.py
   ```

5. Ejecuta la aplicación:
   ```
   python run.py
   ```

6. Accede a la aplicación en tu navegador: http://localhost:5000


## Estructura del Proyecto

```
proyecto_tiendas_flask/
├── app/                      # Código principal de la aplicación
│   ├── models/               # Modelos de datos
│   ├── routes/               # Rutas y controladores
│   ├── services/             # Servicios (geoespacial, CSV, etc.)
│   ├── static/               # Archivos estáticos (CSS, JS, imágenes)
│   ├── templates/            # Plantillas HTML
│   ├── __init__.py           # Inicialización de la aplicación
│   └── config.py             # Configuración de la aplicación
├── tests/                    # Pruebas unitarias
├── .env                      # Variables de entorno
├── .gitignore                # Archivos ignorados por Git
├── docker-compose.yml        # Configuración de Docker Compose
├── Dockerfile                # Configuración de Docker
├── LICENSE                   # Licencia del proyecto
├── README.md                 # Este archivo
├── requirements.txt          # Dependencias de Python
├── run.py                    # Script para ejecutar en desarrollo
├── seed_db.py                # Script para poblar la base de datos
├── run_tests.sh              # Script para ejecutar pruebas
├── start_dev.sh              # Script para iniciar en desarrollo
└── wsgi.py                   # Punto de entrada para WSGI
```

## Uso de la Aplicación

### Para Usuarios

1. Regístrate o inicia sesión en la aplicación
2. Utiliza la barra de búsqueda para encontrar productos
3. Activa tu ubicación para ver las tiendas más cercanas
4. Explora el mapa para ver todas las tiendas disponibles

### Para Dueños de Tiendas

1. Regístrate o inicia sesión en la aplicación
2. Crea una nueva tienda proporcionando su ubicación
3. Añade productos individualmente o carga un archivo CSV
4. Gestiona tu inventario actualizando productos y stock

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.

## Contacto

Para cualquier consulta o sugerencia, por favor contacta a [tu-email@ejemplo.com](mailto:tu-email@ejemplo.com).
