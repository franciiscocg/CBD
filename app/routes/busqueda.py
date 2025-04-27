from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.models.tienda import Tienda
from app.models.producto import Producto
from app.services.geo_service import calcular_distancia, encontrar_tienda_mas_cercana
import json
from bson import ObjectId

busqueda = Blueprint('busqueda', __name__)

@busqueda.route('/')
def index():
    """Ruta principal que redirige a la página de búsqueda"""
    return redirect(url_for('busqueda.buscar'))

@busqueda.route('/buscar')
def buscar():
    """Página de búsqueda de productos"""
    query = request.args.get('q', '')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    
    resultados = []
    tiendas_cercanas = []
    
    if query:
        # Buscar productos que coincidan con la consulta
        productos = Producto.search(query)
        
        if lat and lng and productos:
            # Si tenemos ubicación y productos, encontrar tiendas cercanas
            tiendas_ids = list(set([p.tienda_id for p in productos]))
            tiendas = [Tienda.find_by_id(tid) for tid in tiendas_ids if Tienda.find_by_id(tid)]
            
            # Calcular distancias y ordenar por cercanía
            tiendas_con_distancia = []
            for t in tiendas:
                if t and t.activo: # Asegurarse que la tienda existe y está activa
                    dist = calcular_distancia(lat, lng, t.latitud, t.longitud)
                    tiendas_con_distancia.append((t, dist))
            
            tiendas_cercanas = sorted(tiendas_con_distancia, key=lambda x: x[1])
            
            # Preparar resultados para mostrar (en la página buscar.html, esto podría ser diferente)
            # Esta lógica parece más para la página de resultados que para la API
            # Debería revisarse si buscar.html usa esta ruta directamente o una API
            # buscar.html usa /api/buscar/producto-cercano, así que esta lógica puede no ser relevante aquí
            pass # Lógica de resultados omitida por ahora, ya que buscar.html usa API

        elif productos:
            # Lógica si no hay ubicación, también probablemente no usada por buscar.html
            pass # Lógica omitida
    
    # La plantilla buscar.html parece depender principalmente de JS y APIs
    # Pasar query podría ser útil para pre-rellenar el campo de búsqueda si viene en URL
    return render_template('busqueda/buscar.html', query=query)

@busqueda.route('/mapa')
def mapa():
    """Página de mapa con todas las tiendas"""
    # Esta ruta carga la plantilla mapa.html, que luego usa JS y APIs
    return render_template('busqueda/mapa.html')

@busqueda.route('/api/tiendas-cercanas')
def api_tiendas_cercanas():
    """API para obtener tiendas cercanas en formato JSON"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radio_km = request.args.get('radio', 5, type=int)  # Radio en km
    radio_metros = radio_km * 1000
    
    if not lat or not lng:
        return jsonify({'error': 'Se requieren parámetros lat y lng'}), 400
    
    # Usar find_near del modelo Tienda
    tiendas = Tienda.find_near(lat, lng, radio_metros, {'activo': True})
    
    # Convertir a formato JSON
    tiendas_json = []
    for t in tiendas:
        distancia = calcular_distancia(lat, lng, t.latitud, t.longitud)
        tiendas_json.append({
            'id': str(t._id),
            'nombre': t.nombre,
            'direccion': t.direccion,
            'latitud': t.latitud,
            'longitud': t.longitud,
            'distancia': round(distancia, 2) # Distancia en km
        })
        
    # Ordenar por distancia
    tiendas_json.sort(key=lambda x: x['distancia'])
    
    return jsonify({'resultados': tiendas_json, 'total': len(tiendas_json)})

@busqueda.route('/api/buscar/producto-cercano')
def api_buscar_producto_cercano():
    """API para buscar productos por término y encontrar la tienda más cercana"""
    termino = request.args.get('termino', '')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    
    if not termino:
        return jsonify({'error': 'Se requiere un término de búsqueda'}), 400
    
    if not lat or not lng:
        # Podríamos buscar sin lat/lng, pero la lógica actual requiere ubicación
        return jsonify({'error': 'Se requieren parámetros lat y lng para buscar la tienda más cercana'}), 400
    
    # Buscar productos que coincidan con el término
    productos_encontrados = Producto.search(termino)
    
    if not productos_encontrados:
        return jsonify({'error': f'No se encontraron productos para el término: {termino}'}), 404
    
    # Buscar todas las tiendas activas que tengan estos productos con stock
    tiendas_con_producto_activo = []
    productos_por_tienda = {}
    
    for producto in productos_encontrados:
        if producto.stock > 0:
            tienda = Tienda.find_by_id(producto.tienda_id)
            if tienda and tienda.activo:
                tienda_id_str = str(tienda._id)
                if tienda not in tiendas_con_producto_activo:
                     tiendas_con_producto_activo.append(tienda)
                if tienda_id_str not in productos_por_tienda:
                    productos_por_tienda[tienda_id_str] = []
                # Añadir solo si el nombre coincide exactamente o muy similarmente?
                # Por ahora, añadimos todos los productos encontrados por Producto.search
                productos_por_tienda[tienda_id_str].append(producto)

    if not tiendas_con_producto_activo:
        return jsonify({'error': f'No se encontraron tiendas activas con stock disponible para: {termino}'}), 404
    
    # Encontrar la tienda más cercana de la lista
    tienda_cercana, distancia = encontrar_tienda_mas_cercana(tiendas_con_producto_activo, lat, lng)
    
    if not tienda_cercana:
        # Esto no debería pasar si tiendas_con_producto_activo no está vacía
        return jsonify({'error': 'Error al calcular la tienda más cercana'}), 500
    
    # Obtener los productos de esta tienda cercana que coincidieron con la búsqueda
    productos_tienda_cercana = productos_por_tienda.get(str(tienda_cercana._id), [])
    productos_json = []
    
    for producto in productos_tienda_cercana:
        # Aquí podríamos añadir más detalles si es necesario
        productos_json.append({
            'id': str(producto._id),
            'nombre': producto.nombre,
            'precio': producto.precio,
            'stock': producto.stock,
            'imagen': producto.imagen  # Corregido: usar el atributo imagen directamente
            # 'categoria': producto.categoria,
            # 'descripcion': producto.descripcion
        })
    
    return jsonify({
        'tienda': {
            'id': str(tienda_cercana._id),
            'nombre': tienda_cercana.nombre,
            'direccion': tienda_cercana.direccion,
            'latitud': tienda_cercana.latitud,
            'longitud': tienda_cercana.longitud,
            'distancia': round(distancia, 2) # Distancia en km
        },
        'productos': productos_json
    })

# --- NUEVO ENDPOINT --- 
@busqueda.route('/api/buscar/productos-en-radio')
def api_buscar_productos_en_radio():
    """API para buscar todas las tiendas con un producto específico dentro de un radio"""
    termino = request.args.get('termino', '')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radio_km = request.args.get('radio', 5, type=int) # Radio en km
    radio_metros = radio_km * 1000

    if not termino:
        return jsonify({'error': 'Se requiere un término de búsqueda'}), 400
    
    if not lat or not lng:
        return jsonify({'error': 'Se requieren parámetros lat y lng para buscar en radio'}), 400

    # 1. Buscar productos que coincidan con el término
    productos_encontrados = Producto.search(termino)
    if not productos_encontrados:
        return jsonify({'resultados': [], 'total': 0, 'mensaje': f'No se encontraron productos para el término: {termino}'})

    # 2. Obtener IDs de tiendas únicas que tienen estos productos con stock
    tienda_ids_con_producto_stock = set()
    productos_info = {} # Guardar info relevante del producto por tienda_id y producto_id
    for p in productos_encontrados:
        if p.stock > 0:
            tienda_id_str = str(p.tienda_id)
            tienda_ids_con_producto_stock.add(p.tienda_id) # Guardamos ObjectId
            if tienda_id_str not in productos_info:
                productos_info[tienda_id_str] = {}
            # Guardamos el primer producto encontrado por tienda que coincida (podría haber varios)
            # Idealmente, la búsqueda debería ser más específica o devolver todos los productos coincidentes por tienda
            if termino.lower() in p.nombre.lower(): # Filtro adicional por nombre
                 if p._id not in productos_info[tienda_id_str]:
                     productos_info[tienda_id_str][str(p._id)] = {
                         'id': str(p._id),
                         'nombre': p.nombre,
                         'precio': p.precio
                     }

    if not tienda_ids_con_producto_stock:
         return jsonify({'resultados': [], 'total': 0, 'mensaje': f'No se encontraron tiendas con stock disponible para: {termino}'})

    # 3. Buscar tiendas activas dentro del radio que estén en la lista de IDs
    query_tiendas = {
        '_id': {'$in': list(tienda_ids_con_producto_stock)},
        'activo': True,
        'ubicacion': {
            '$near': {
                '$geometry': {
                    'type': 'Point',
                    'coordinates': [lng, lat]
                },
                '$maxDistance': radio_metros
            }
        }
    }
    
    cursor_tiendas = Tienda.collection.find(query_tiendas)
    tiendas_en_radio = [Tienda.from_dict(data) for data in cursor_tiendas]

    # 4. Formatear resultados
    resultados_finales = []
    for tienda in tiendas_en_radio:
        tienda_id_str = str(tienda._id)
        productos_de_tienda = productos_info.get(tienda_id_str, {})
        
        # Solo incluir tienda si tiene productos que coinciden con el término buscado
        if productos_de_tienda:
            distancia = calcular_distancia(lat, lng, tienda.latitud, tienda.longitud)
            resultados_finales.append({
                'tienda': {
                    'id': tienda_id_str,
                    'nombre': tienda.nombre,
                    'direccion': tienda.direccion,
                    'latitud': tienda.latitud,
                    'longitud': tienda.longitud,
                    'distancia': round(distancia, 2) # Distancia en km
                },
                # Devolver lista de productos coincidentes en esta tienda
                'productos': list(productos_de_tienda.values()) 
            })

    # Ordenar por distancia
    resultados_finales.sort(key=lambda x: x['tienda']['distancia'])

    return jsonify({'resultados': resultados_finales, 'total': len(resultados_finales)})
