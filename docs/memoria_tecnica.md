# Memoria Técnica: TiendasGeo

## 1. Introducción

### 1.1 Contexto del Proyecto

TiendasGeo es una aplicación web diseñada para resolver un problema común: encontrar productos específicos en tiendas cercanas a la ubicación del usuario. La aplicación utiliza tecnologías geoespaciales para localizar tiendas y permite a los dueños de establecimientos cargar y gestionar su inventario de manera sencilla mediante archivos CSV.

### 1.2 Objetivos

- Desarrollar una aplicación web que permita buscar productos y mostrar la tienda más cercana donde están disponibles
- Implementar una base de datos NoSQL (MongoDB) con capacidades geoespaciales
- Crear un sistema para que los dueños de tiendas puedan cargar su inventario desde archivos CSV
- Diseñar una interfaz de usuario intuitiva con mapas interactivos
- Proporcionar una solución escalable y de alto rendimiento

### 1.3 Alcance

La aplicación incluye:
- Sistema de autenticación y registro de usuarios
- Gestión de tiendas con ubicaciones geoespaciales
- Carga y gestión de productos
- Búsqueda de productos y tiendas cercanas
- Visualización de resultados en mapas interactivos

## 2. Arquitectura del Sistema

### 2.1 Visión General

TiendasGeo utiliza una arquitectura basada en Flask como framework web y MongoDB como base de datos NoSQL. Esta combinación proporciona flexibilidad, rendimiento y soporte nativo para operaciones geoespaciales.

### 2.2 Componentes Principales

- **Frontend**: HTML, CSS, JavaScript, Bootstrap 5, Leaflet.js
- **Backend**: Flask, PyMongo
- **Base de datos**: MongoDB
- **Servicios**: Geoespacial, Procesamiento CSV
- **Despliegue**: Docker, Docker Compose

### 2.3 Diagrama de Arquitectura

```
[Usuario] <-> [Navegador Web] <-> [Servidor Flask] <-> [MongoDB]
                                       |
                                       v
                            [Servicios (Geo, CSV, etc.)]
```

## 3. Tecnologías Utilizadas

### 3.1 Backend

- **Flask**: Framework web ligero y flexible para Python
- **PyMongo**: Driver oficial de MongoDB para Python
- **Flask-Login**: Gestión de sesiones de usuario
- **Python-dotenv**: Gestión de variables de entorno

### 3.2 Base de Datos

- **MongoDB**: Base de datos NoSQL orientada a documentos
- **Índices geoespaciales**: Para consultas de proximidad
- **Consultas geoespaciales**: $near, $geoWithin, etc.

### 3.3 Frontend

- **Bootstrap 5**: Framework CSS para diseño responsive
- **Leaflet.js**: Biblioteca JavaScript para mapas interactivos
- **Font Awesome**: Iconos vectoriales
- **JavaScript**: Interactividad del lado del cliente

### 3.4 Herramientas de Desarrollo y Despliegue

- **Docker**: Contenedorización de la aplicación
- **Docker Compose**: Orquestación de contenedores
- **Git**: Control de versiones
- **Pytest**: Framework de pruebas para Python

## 4. Modelo de Datos

### 4.1 Colecciones de MongoDB

#### 4.1.1 Usuarios
```json
{
  "_id": ObjectId("..."),
  "username": "usuario_ejemplo",
  "email": "usuario@ejemplo.com",
  "password": "hash_contraseña"
}
```

#### 4.1.2 Tiendas
```json
{
  "_id": ObjectId("..."),
  "nombre": "Tienda Ejemplo",
  "descripcion": "Descripción de la tienda",
  "direccion": "Calle Ejemplo, 123",
  "telefono": "+34123456789",
  "email": "tienda@ejemplo.com",
  "sitio_web": "https://tienda-ejemplo.com",
  "horario": "Lun-Vie: 9:00-20:00",
  "propietario_id": "...",
  "latitud": 40.416775,
  "longitud": -3.703790,
  "ubicacion": {
    "type": "Point",
    "coordinates": [-3.703790, 40.416775]
  },
  "categorias": ["Electrónica", "Informática"],
  "fecha_registro": ISODate("2025-04-21T08:00:00Z"),
  "fecha_actualizacion": ISODate("2025-04-21T08:00:00Z"),
  "activo": true
}
```

#### 4.1.3 Productos
```json
{
  "_id": ObjectId("..."),
  "nombre": "Producto Ejemplo",
  "descripcion": "Descripción del producto",
  "codigo": "PROD001",
  "precio": 99.99,
  "stock": 10,
  "tienda_id": ObjectId("..."),
  "categoria": "Electrónica",
  "imagen": "/static/uploads/producto001.jpg",
  "fecha_creacion": ISODate("2025-04-21T08:00:00Z"),
  "fecha_actualizacion": ISODate("2025-04-21T08:00:00Z"),
  "activo": true
}
```

### 4.2 Índices

- Índice geoespacial en `tiendas.ubicacion`: `{"ubicacion": "2dsphere"}`
- Índice de texto en `productos.nombre`: `{"nombre": "text"}`
- Índice compuesto en `productos.tienda_id` y `productos.categoria`

## 5. Implementación

### 5.1 Estructura del Proyecto

La aplicación sigue una estructura modular:

```
app/
├── models/          # Modelos de datos
├── routes/          # Rutas y controladores
├── services/        # Servicios (geoespacial, CSV)
├── static/          # Archivos estáticos
├── templates/       # Plantillas HTML
├── __init__.py      # Inicialización de la aplicación
└── config.py        # Configuración
```

### 5.2 Modelos

Los modelos implementan la lógica de negocio y la interacción con la base de datos:

- **Tienda**: Gestiona información de tiendas y operaciones geoespaciales
- **Producto**: Gestiona información de productos y búsquedas
- **User**: Gestiona autenticación y perfiles de usuario

### 5.3 Servicios

- **GeoService**: Cálculo de distancias y búsqueda de tiendas cercanas
- **CSVService**: Procesamiento de archivos CSV para carga de productos

### 5.4 Rutas

- **/auth/**: Registro, login y gestión de usuarios
- **/tiendas/**: CRUD de tiendas y operaciones geoespaciales
- **/productos/**: CRUD de productos y carga CSV
- **/buscar/**: Búsqueda de productos y tiendas cercanas

## 6. Funcionalidades Principales

### 6.1 Búsqueda Geoespacial

La búsqueda geoespacial utiliza los índices `2dsphere` de MongoDB para encontrar tiendas cercanas a una ubicación:

```python
def find_near(cls, lat, lng, max_distance=5000, query=None):
    """
    Busca tiendas cercanas a una ubicación.
    max_distance: distancia máxima en metros
    query: filtros adicionales
    """
    query = query or {}
    query['ubicacion'] = {
        '$near': {
            '$geometry': {
                'type': 'Point',
                'coordinates': [lng, lat]
            },
            '$maxDistance': max_distance
        }
    }
    
    cursor = cls.collection.find(query)
    return [cls.from_dict(data) for data in cursor]
```

### 6.2 Carga de Productos desde CSV

El servicio de procesamiento CSV permite a los dueños de tiendas cargar su inventario:

```python
def procesar_csv(archivo, tienda_id):
    """
    Procesa un archivo CSV y crea/actualiza productos en la base de datos.
    """
    # Leer CSV con pandas
    df = pd.read_csv(archivo)
    
    # Verificar columnas requeridas
    columnas_requeridas = ['nombre', 'precio', 'stock']
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"El archivo CSV debe contener la columna '{col}'")
    
    # Procesar cada fila...
```

### 6.3 Interfaz de Usuario

La interfaz utiliza Bootstrap 5 para un diseño responsive y Leaflet.js para mapas interactivos:

```javascript
// Inicializar mapa
function initMap() {
    // Crear mapa centrado en España
    map = L.map('map').setView([40.416775, -3.703790], 6);
    
    // Añadir capa de OpenStreetMap
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
    }).addTo(map);
    
    // Configurar eventos...
}
```

## 7. Despliegue

### 7.1 Entorno de Desarrollo

Para el entorno de desarrollo, se utiliza un servidor Flask integrado:

```
python seed_db.py
python run.py
```


## 8. Pruebas

### 8.1 Pruebas Unitarias

Se implementaron pruebas unitarias con Pytest para verificar la funcionalidad:

```python
def test_calcular_distancia():
    """Prueba la función de cálculo de distancia entre dos puntos geográficos."""
    # Madrid a Barcelona (aproximadamente 504 km)
    distancia = calcular_distancia(40.4168, -3.7038, 41.3851, 2.1734)
    assert 500 < distancia < 510
```

### 8.2 Pruebas de Integración

Las pruebas de integración verifican la interacción entre componentes:

```python
def test_buscar_page(client):
    """Prueba que la página de búsqueda se muestra correctamente."""
    response = client.get('/buscar')
    assert response.status_code == 200
```

## 9. Conclusiones y Trabajo Futuro

### 9.1 Logros

- Implementación exitosa de una aplicación web con funcionalidades geoespaciales
- Integración directa con MongoDB para operaciones geoespaciales nativas
- Interfaz de usuario intuitiva con mapas interactivos
- Sistema de carga de productos desde CSV

### 9.2 Lecciones Aprendidas

- La importancia de elegir las tecnologías adecuadas para cada requisito
- Las ventajas de utilizar MongoDB para datos geoespaciales
- La flexibilidad de Flask para crear aplicaciones web modulares

### 9.3 Trabajo Futuro

- Implementación de una API REST completa
- Desarrollo de aplicaciones móviles nativas
- Integración con servicios de rutas y navegación
- Análisis de datos y recomendaciones personalizadas

## 10. Referencias

- Documentación de Flask: https://flask.palletsprojects.com/
- Documentación de MongoDB: https://docs.mongodb.com/
- Documentación de PyMongo: https://pymongo.readthedocs.io/
- Documentación de Leaflet: https://leafletjs.com/reference.html
- Documentación de Bootstrap: https://getbootstrap.com/docs/5.0/
