from datetime import datetime
from bson import ObjectId
from app import mongo

class Producto:
    """
    Modelo para almacenar información de productos.
    """
    collection = mongo.db.productos
    
    def __init__(self, nombre, precio, stock, tienda_id, 
                 descripcion=None, codigo=None, categoria=None, 
                 imagen=None, activo=True, _id=None):
        self.nombre = nombre
        self.descripcion = descripcion
        self.codigo = codigo
        self.precio = precio
        self.stock = stock
        self.tienda_id = tienda_id
        self.categoria = categoria
        self.imagen = imagen
        self.fecha_creacion = datetime.utcnow()
        self.fecha_actualizacion = datetime.utcnow()
        self.activo = activo
        self._id = _id
    
    def to_dict(self):
        """Convierte el objeto a un diccionario para MongoDB."""
        return {
            'nombre': self.nombre,
            'descripcion': self.descripcion,
            'codigo': self.codigo,
            'precio': self.precio,
            'stock': self.stock,
            'tienda_id': self.tienda_id,
            'categoria': self.categoria,
            'imagen': self.imagen,
            'fecha_creacion': self.fecha_creacion,
            'fecha_actualizacion': self.fecha_actualizacion,
            'activo': self.activo
        }
    
    @classmethod
    def from_dict(cls, data):
        """Crea un objeto Producto desde un diccionario de MongoDB."""
        return cls(
            nombre=data.get('nombre'),
            descripcion=data.get('descripcion'),
            codigo=data.get('codigo'),
            precio=data.get('precio'),
            stock=data.get('stock'),
            tienda_id=data.get('tienda_id'),
            categoria=data.get('categoria'),
            imagen=data.get('imagen'),
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
        """Busca un producto por su ID."""
        data = cls.collection.find_one({'_id': ObjectId(id)})
        return cls.from_dict(data) if data else None
    
    @classmethod
    def find_by_tienda(cls, tienda_id, categoria=None, activo=None):
        """Busca productos por tienda, opcionalmente filtrados."""
        query = {'tienda_id': tienda_id}
        if categoria:
            query['categoria'] = categoria
        if activo is not None:
            query['activo'] = activo
        
        cursor = cls.collection.find(query)
        return [cls.from_dict(data) for data in cursor]
    
    @classmethod
    def search(cls, termino, tienda_id=None, activo=True):
        """Busca productos por término de búsqueda."""
        query = {
            '$or': [
                {'nombre': {'$regex': termino, '$options': 'i'}},
                {'descripcion': {'$regex': termino, '$options': 'i'}},
                {'codigo': {'$regex': termino, '$options': 'i'}}
            ],
            'activo': activo
        }
        
        if tienda_id:
            query['tienda_id'] = tienda_id
        
        cursor = cls.collection.find(query)
        return [cls.from_dict(data) for data in cursor]

    def delete(self):
        """Elimina el objeto de la base de datos."""
        if self._id:
            result = self.collection.delete_one({"_id": self._id})
            return result.deleted_count > 0
        return False

