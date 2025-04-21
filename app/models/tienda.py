from datetime import datetime
from bson import ObjectId
from app import mongo

class Tienda:
    """
    Modelo para almacenar información de tiendas con datos geoespaciales.
    """
    collection = mongo.db.tiendas
    
    def __init__(self, nombre, direccion, latitud, longitud, propietario_id, 
                 descripcion=None, telefono=None, email=None, sitio_web=None, 
                 horario=None, categorias=None, activo=True, _id=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.direccion = direccion
        self.telefono = telefono
        self.email = email
        self.sitio_web = sitio_web
        self.horario = horario
        self.propietario_id = propietario_id
        self.latitud = latitud
        self.longitud = longitud
        self.ubicacion = {
            'type': 'Point',
            'coordinates': [longitud, latitud]
        }
        self.categorias = categorias or []
        self.fecha_registro = datetime.utcnow()
        self.fecha_actualizacion = datetime.utcnow()
        self.activo = activo
        self._id = _id
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para MongoDB."""
        return {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'direccion': self.direccion,
            'telefono': self.telefono,
            'email': self.email,
            'sitio_web': self.sitio_web,
            'horario': self.horario,
            'propietario_id': self.propietario_id,
            'latitud': self.latitud,
            'longitud': self.longitud,
            'ubicacion': self.ubicacion,
            'categorias': self.categorias,
            'fecha_registro': self.fecha_registro,
            'fecha_actualizacion': self.fecha_actualizacion,
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Tienda desde un diccionario de MongoDB."""
        return cls(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            direccion=data.get('direccion'),
            telefono=data.get('telefono'),
            email=data.get('email'),
            sitio_web=data.get('sitio_web'),
            horario=data.get('horario'),
            propietario_id=data.get('propietario_id'),
            latitud=data.get('latitud'),
            longitud=data.get('longitud'),
            categorias=data.get('categorias', []),
            activo=data.get('activo', True),
            _id=data.get('_id')
        )
    
    def save(self):
        """Guarda el objeto en la base de datos."""
        data = self.to_dict()
        if self._id:
            data['fecha_actualizacion'] = datetime.utcnow()
            self.collection.update_one({'_id': self._id}, {'$set': data})
        else:
            result = self.collection.insert_one(data)
            self._id = result.inserted_id
        return self._id
    
    @classmethod
    def find_by_id(cls, id):
        """Busca una tienda por su ID."""
        data = cls.collection.find_one({'_id': ObjectId(id)})
        return cls.from_dict(data) if data else None
    
    @classmethod
    def find_all(cls, propietario_id=None, activo=None):
        """Busca todas las tiendas, opcionalmente filtradas."""
        query = {}
        if propietario_id:
            query['propietario_id'] = propietario_id
        if activo is not None:
            query['activo'] = activo
        
        cursor = cls.collection.find(query)
        return [cls.from_dict(data) for data in cursor]
    
    @classmethod
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
    
    def distancia_a(self, lat, lng):
        """
        Calcula la distancia aproximada en kilómetros a las coordenadas dadas.
        Utiliza la fórmula de Haversine para el cálculo.
        """
        from math import radians, cos, sin, asin, sqrt
        
        # Convertir coordenadas a radianes
        lon1, lat1, lon2, lat2 = map(radians, [self.longitud, self.latitud, lng, lat])
        
        # Fórmula de Haversine
        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
        c = 2 * asin(sqrt(a))
        r = 6371  # Radio de la Tierra en kilómetros
        
        return c * r
