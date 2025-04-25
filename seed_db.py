from datetime import datetime
from pymongo import MongoClient
from werkzeug.security import generate_password_hash

client = MongoClient("mongodb://localhost:27017/")
db = client["tiendas_geo_db"]

usuarios_col = db["users"]
tiendas_col = db["tiendas"]
productos_col = db["productos"]

# Limpiar colecciones
usuarios_col.delete_many({})
tiendas_col.delete_many({})
productos_col.delete_many({})

# Crear usuarios
usuarios = [
    {
        "username": "usuario1",
        "email": "usuario1@correo.com",
        "password": generate_password_hash("usuario1"),
    },
    {
        "username": "usuario2",
        "email": "usuario2@correo.com",
        "password": generate_password_hash("usuario2"),
    },
    {
        "username": "usuario3",
        "email": "usuario3@correo.com",
        "password": generate_password_hash("usuario3"),
    },
    {
        "username": "usuario4",
        "email": "usuario4@correo.com",
        "password": generate_password_hash("usuario4"),
    },
    {
        "username": "usuario5",
        "email": "usuario5@correo.com",
        "password": generate_password_hash("usuario5"),
    },
    {
        "username": "usuario6",
        "email": "usuario6@correo.com",
        "password": generate_password_hash("usuario6"),
    },
    {
        "username": "usuario7",
        "email": "usuario7@correo.com",
        "password": generate_password_hash("usuario7"),
    }
]
usuario_ids = usuarios_col.insert_many(usuarios).inserted_ids

# Datos de tiendas
tiendas_data = [
    # Sevilla - Reina Mercedes
    ("Papelería Imperial", "Av. Reina Mercedes 31", 37.3598, -5.9865),
    ("Librería Reina", "Av. Reina Mercedes 35", 37.3602, -5.9859),
    ("Copistería Sur", "Av. Reina Mercedes 37", 37.3606, -5.9854),
    ("Oficina Express", "Av. Reina Mercedes 39", 37.3610, -5.9849),
    ("Estudios y Más", "Av. Reina Mercedes 41", 37.3613, -5.9844),
    # Alcalá de Guadaíra
    ("Papelería Alcalá", "Calle La Mina 14", 37.3360, -5.8450),
    ("OfiAlcalá", "Calle Silos 22", 37.3380, -5.8475)
]

# Funciones auxiliares
def crear_tienda(nombre, direccion, lat, lng, propietario_id, index):
    return {
        "nombre": nombre,
        "descripcion": f"Tienda ubicada en {direccion}",
        "direccion": direccion,
        "telefono": f"9540000{index}",
        "email": f"{nombre.lower().replace(' ', '')}@ejemplo.com",
        "sitio_web": f"http://{nombre.lower().replace(' ', '')}.com",
        "horario": "09:00 - 20:00",
        "propietario_id": str(propietario_id),
        "latitud": lat,
        "longitud": lng,
        "ubicacion": {"type": "Point", "coordinates": [lng, lat]},
        "categorias": ["Papelería", "Oficina"],
        "activo": True,
        "fecha_registro": datetime.utcnow()
    }

def crear_productos(tienda_id):
    productos = [
        {
            "nombre": "Cuaderno A4",
            "descripcion": "Cuaderno de 100 hojas",
            "codigo": "CUAD100",
            "precio": 3.95,
            "stock": 20,
            "tienda_id": tienda_id,
            "categoria": "Papelería",
            "imagen": None,
            "fecha_creacion": datetime.utcnow(),
            "fecha_actualizacion": datetime.utcnow(),
            "activo": True
        },
        {
            "nombre": "Bolígrafo azul",
            "descripcion": "Bolígrafo tinta azul marca BIC",
            "codigo": "BOLBIC",
            "precio": 1.20,
            "stock": 50,
            "tienda_id": tienda_id,
            "categoria": "Papelería",
            "imagen": None,
            "fecha_creacion": datetime.utcnow(),
            "fecha_actualizacion": datetime.utcnow(),
            "activo": True
        }
    ]
    productos_col.insert_many(productos)

# Insertar tiendas y productos
for i, (nombre, direccion, lat, lng) in enumerate(tiendas_data):
    propietario_id = usuario_ids[i]
    tienda = crear_tienda(nombre, direccion, lat, lng, propietario_id, i)
    tienda_id = tiendas_col.insert_one(tienda).inserted_id
    crear_productos(tienda_id)

print("✅ Usuarios, tiendas y productos añadidos correctamente.")
