from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, current_app
from flask_login import login_required, current_user
from app.models.tienda import Tienda
from app.models.producto import Producto
from app.services.geo_service import calcular_distancia, encontrar_tienda_mas_cercana
import json

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
                dist = calcular_distancia(lat, lng, t.latitud, t.longitud)
                tiendas_con_distancia.append((t, dist))
            
            tiendas_cercanas = sorted(tiendas_con_distancia, key=lambda x: x[1])
            
            # Preparar resultados para mostrar
            for tienda, distancia in tiendas_cercanas:
                productos_tienda = [p for p in productos if p.tienda_id == tienda._id]
                if productos_tienda:
                    resultados.append({
                        'tienda': tienda,
                        'productos': productos_tienda,
                        'distancia': distancia
                    })
        elif productos:
            # Si no tenemos ubicación, mostrar todos los productos agrupados por tienda
            tiendas_dict = {}
            for p in productos:
                tienda = Tienda.find_by_id(p.tienda_id)
                if tienda:
                    if tienda._id not in tiendas_dict:
                        tiendas_dict[tienda._id] = {
                            'tienda': tienda,
                            'productos': [],
                            'distancia': None
                        }
                    tiendas_dict[tienda._id]['productos'].append(p)
            
            resultados = list(tiendas_dict.values())
    
    return render_template('busqueda/buscar.html', 
                          query=query, 
                          resultados=resultados, 
                          tiendas_cercanas=tiendas_cercanas,
                          lat=lat,
                          lng=lng)

@busqueda.route('/mapa')
def mapa():
    """Página de mapa con todas las tiendas"""
    tiendas = Tienda.find_all()
    
    # Convertir tiendas a GeoJSON para el mapa
    features = []
    for t in tiendas:
        features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [t.longitud, t.latitud]
            },
            'properties': {
                'id': str(t._id),
                'nombre': t.nombre,
                'direccion': t.direccion,
                'telefono': t.telefono or '',
                'url': url_for('tiendas.detalle_tienda', tienda_id=t._id)
            }
        })
    
    geojson = {
        'type': 'FeatureCollection',
        'features': features
    }
    
    return render_template('busqueda/mapa.html', 
                          tiendas=tiendas,
                          tiendas_geojson=json.dumps(geojson))

@busqueda.route('/api/tiendas-cercanas')
def api_tiendas_cercanas():
    """API para obtener tiendas cercanas en formato JSON"""
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    radio = request.args.get('radio', 5000, type=int)  # Radio en metros, por defecto 5km
    
    if not lat or not lng:
        return jsonify({'error': 'Se requieren parámetros lat y lng'}), 400
    
    tiendas = Tienda.find_near(lat, lng, radio)
    
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
            'distancia': round(distancia, 2)
        })
    
    return jsonify(tiendas_json)

@busqueda.route('/api/buscar/producto-cercano')
def api_buscar_producto_cercano():
    """API para buscar productos por término y encontrar la tienda más cercana"""
    termino = request.args.get('termino', '')
    lat = request.args.get('lat', type=float)
    lng = request.args.get('lng', type=float)
    
    if not termino:
        return jsonify({'error': 'Se requiere un término de búsqueda'}), 400
    
    if not lat or not lng:
        return jsonify({'error': 'Se requieren parámetros lat y lng'}), 400
    
    # Buscar productos que coincidan con el término
    productos = Producto.search(termino)
    
    if not productos:
        return jsonify({'error': f'No se encontraron productos para el término: {termino}'}), 404
    
    # Buscar todas las tiendas que tengan estos productos
    tiendas_con_productos = []
    productos_por_tienda = {}
    
    for producto in productos:
        if producto.stock > 0:  # Solo considerar productos con stock disponible
            tienda = Tienda.find_by_id(producto.tienda_id)
            if tienda and tienda.activo:
                tienda_id = str(tienda._id)
                if tienda_id not in productos_por_tienda:
                    tiendas_con_productos.append(tienda)
                    productos_por_tienda[tienda_id] = []
                productos_por_tienda[tienda_id].append(producto)
    
    if not tiendas_con_productos:
        return jsonify({'error': f'No se encontraron tiendas con productos disponibles para: {termino}'}), 404
    
    # Encontrar la tienda más cercana
    tienda_cercana, distancia = encontrar_tienda_mas_cercana(tiendas_con_productos, lat, lng)
    
    if not tienda_cercana:
        return jsonify({'error': 'Error al calcular la tienda más cercana'}), 500
    
    # Obtener los productos de esta tienda
    productos_tienda = productos_por_tienda[str(tienda_cercana._id)]
    productos_json = []
    
    for producto in productos_tienda:
        productos_json.append({
            'id': str(producto._id),
            'nombre': producto.nombre,
            'precio': producto.precio,
            'stock': producto.stock,
            'codigo': producto.codigo,
            'categoria': producto.categoria
        })
    
    return jsonify({
        'tienda': {
            'id': str(tienda_cercana._id),
            'nombre': tienda_cercana.nombre,
            'direccion': tienda_cercana.direccion,
            'latitud': tienda_cercana.latitud,
            'longitud': tienda_cercana.longitud,
            'distancia': round(distancia, 2)
        },
        'productos': productos_json,
        'total_productos': len(productos_json)
    })
