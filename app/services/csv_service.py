import pandas as pd
from app.models.producto import Producto
from bson import ObjectId

def procesar_csv(archivo, tienda_id):
    """
    Procesa un archivo CSV y crea/actualiza productos en la base de datos.
    
    Args:
        archivo: Objeto de archivo CSV
        tienda_id: ID de la tienda a la que pertenecen los productos
        
    Returns:
        dict: Resultados del procesamiento (creados, actualizados, errores)
    """
    # Leer CSV con pandas
    df = pd.read_csv(archivo)
    
    # Verificar columnas requeridas
    columnas_requeridas = ['nombre', 'precio', 'stock']
    for col in columnas_requeridas:
        if col not in df.columns:
            raise ValueError(f"El archivo CSV debe contener la columna '{col}'")
    
    # Inicializar contadores
    creados = 0
    actualizados = 0
    errores = 0
    
    # Procesar cada fila
    for _, row in df.iterrows():
        try:
            # Buscar producto existente por código o nombre
            producto = None
            if 'codigo' in row and pd.notna(row['codigo']):
                producto = Producto.collection.find_one({
                    'codigo': row['codigo'],
                    'tienda_id': ObjectId(tienda_id)
                })
            
            if not producto and 'nombre' in row:
                producto = Producto.collection.find_one({
                    'nombre': row['nombre'],
                    'tienda_id': ObjectId(tienda_id)
                })
            
            # Crear o actualizar producto
            if producto:
                # Actualizar producto existente
                producto_obj = Producto.from_dict(producto)
                producto_obj.nombre = row['nombre']
                if 'descripcion' in row and pd.notna(row['descripcion']):
                    producto_obj.descripcion = row['descripcion']
                if 'codigo' in row and pd.notna(row['codigo']):
                    producto_obj.codigo = row['codigo']
                producto_obj.precio = float(row['precio'])
                producto_obj.stock = int(row['stock'])
                if 'categoria' in row and pd.notna(row['categoria']):
                    producto_obj.categoria = row['categoria']
                
                producto_obj.save()
                actualizados += 1
            else:
                # Crear nuevo producto
                producto_data = {
                    'nombre': row['nombre'],
                    'precio': float(row['precio']),
                    'stock': int(row['stock']),
                    'tienda_id': ObjectId(tienda_id)
                }
                
                if 'descripcion' in row and pd.notna(row['descripcion']):
                    producto_data['descripcion'] = row['descripcion']
                if 'codigo' in row and pd.notna(row['codigo']):
                    producto_data['codigo'] = row['codigo']
                if 'categoria' in row and pd.notna(row['categoria']):
                    producto_data['categoria'] = row['categoria']
                
                producto_obj = Producto(**producto_data)
                producto_obj.save()
                creados += 1
        
        except Exception as e:
            errores += 1
            continue
    
    return {
        'creados': creados,
        'actualizados': actualizados,
        'errores': errores
    }
