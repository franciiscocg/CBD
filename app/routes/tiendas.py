from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app.models.tienda import Tienda
from app.models.producto import Producto
from app.services.geo_service import calcular_distancia, encontrar_tienda_mas_cercana
from bson import ObjectId

tiendas = Blueprint('tiendas', __name__)

@tiendas.route('/tiendas')
@login_required
def listar_tiendas():
    """Lista las tiendas del usuario actual."""
    tiendas_lista = Tienda.find_all(propietario_id=current_user.id)
    return render_template('tiendas/listar.html', tiendas=tiendas_lista)

@tiendas.route('/tiendas/crear', methods=['GET', 'POST'])
@login_required
def crear_tienda():
    """Crea una nueva tienda."""
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        direccion = request.form.get('direccion')
        latitud = float(request.form.get('latitud'))
        longitud = float(request.form.get('longitud'))
        telefono = request.form.get('telefono')
        email = request.form.get('email')
        sitio_web = request.form.get('sitio_web')
        horario = request.form.get('horario')
        categorias = request.form.get('categorias', '').split(',')
        categorias = [cat.strip() for cat in categorias if cat.strip()]
        
        tienda = Tienda(
            nombre=nombre,
            descripcion=descripcion,
            direccion=direccion,
            latitud=latitud,
            longitud=longitud,
            telefono=telefono,
            email=email,
            sitio_web=sitio_web,
            horario=horario,
            categorias=categorias,
            propietario_id=current_user.id
        )
        
        tienda.save()
        flash('Tienda creada correctamente', 'success')
        return redirect(url_for('tiendas.detalle_tienda', tienda_id=str(tienda._id)))
    
    return render_template('tiendas/crear.html')

@tiendas.route('/tiendas/<tienda_id>')
@login_required
def detalle_tienda(tienda_id):
    """Muestra los detalles de una tienda."""
    tienda = Tienda.find_by_id(tienda_id)
    
    if not tienda or str(tienda.propietario_id) != str(current_user.id):
        flash('Tienda no encontrada o no tienes permiso para ver esta tienda', 'danger')
        return redirect(url_for('tiendas.listar_tiendas'))
    
    productos = Producto.find_by_tienda(ObjectId(tienda_id))
    
    return render_template('tiendas/detalle.html', tienda=tienda, productos=productos)

@tiendas.route('/tiendas/editar/<tienda_id>', methods=['GET', 'POST'])
@login_required
def editar_tienda(tienda_id):
    """Edita una tienda existente."""
    tienda = Tienda.find_by_id(tienda_id)
    
    if not tienda or str(tienda.propietario_id) != str(current_user.id):
        flash('Tienda no encontrada o no tienes permiso para modificar esta tienda', 'danger')
        return redirect(url_for('tiendas.listar_tiendas'))
    
    if request.method == 'POST':
        tienda.nombre = request.form.get('nombre')
        tienda.descripcion = request.form.get('descripcion')
        tienda.direccion = request.form.get('direccion')
        tienda.latitud = float(request.form.get('latitud'))
        tienda.longitud = float(request.form.get('longitud'))
        tienda.telefono = request.form.get('telefono')
        tienda.email = request.form.get('email')
        tienda.sitio_web = request.form.get('sitio_web')
        tienda.horario = request.form.get('horario')
        categorias = request.form.get('categorias', '').split(',')
        tienda.categorias = [cat.strip() for cat in categorias if cat.strip()]
        
        # Actualizar ubicación geoespacial
        tienda.ubicacion = {
            'type': 'Point',
            'coordinates': [tienda.longitud, tienda.latitud]
        }
        
        tienda.save()
        flash('Tienda actualizada correctamente', 'success')
        return redirect(url_for('tiendas.detalle_tienda', tienda_id=tienda_id))
    
    return render_template('tiendas/editar.html', tienda=tienda)

@tiendas.route('/tiendas/publicas')
def tiendas_publicas():
    """Muestra un listado de todas las tiendas públicas."""
    tiendas_lista = Tienda.find_all(activo=True)
    return render_template('tiendas/publicas.html', tiendas=tiendas_lista)

@tiendas.route('/tiendas/mapa')
def mapa_tiendas():
    """Muestra un mapa con todas las tiendas."""
    tiendas_lista = Tienda.find_all(activo=True)
    return render_template('tiendas/mapa.html', tiendas=tiendas_lista)

@tiendas.route('/api/tiendas/cercanas')
def api_tiendas_cercanas():
    """API para buscar tiendas cercanas."""
    lat = float(request.args.get('lat', 0))
    lng = float(request.args.get('lng', 0))
    radio = int(request.args.get('radio', 5))
    
    # Convertir radio de km a metros
    radio_metros = radio * 1000
    
    tiendas_cercanas = Tienda.find_near(lat, lng, radio_metros, {'activo': True})
    
    # Formatear resultados para JSON
    resultados = []
    for tienda in tiendas_cercanas:
        distancia = calcular_distancia(lat, lng, tienda.latitud, tienda.longitud)
        resultados.append({
            'id': str(tienda._id),
            'nombre': tienda.nombre,
            'direccion': tienda.direccion,
            'latitud': tienda.latitud,
            'longitud': tienda.longitud,
            'distancia': round(distancia, 2)
        })
    
    # Ordenar por distancia
    resultados.sort(key=lambda x: x['distancia'])
    
    return jsonify({'resultados': resultados, 'total': len(resultados)})

@tiendas.route('/api/tiendas/producto-cercano')
def api_producto_cercano():
    """API para buscar la tienda más cercana con un producto específico."""
    lat = float(request.args.get('lat', 0))
    lng = float(request.args.get('lng', 0))
    producto_id = request.args.get('producto_id')
    
    if not producto_id:
        return jsonify({'error': 'Se requiere el ID del producto'}), 400
    
    producto = Producto.find_by_id(producto_id)
    if not producto:
        return jsonify({'error': 'Producto no encontrado'}), 404
    
    # Buscar todas las tiendas que tengan este producto
    tiendas_con_producto = []
    productos_similares = Producto.search(producto.nombre)
    
    for prod in productos_similares:
        if prod.stock > 0:  # Solo considerar tiendas con stock disponible
            tienda = Tienda.find_by_id(prod.tienda_id)
            if tienda and tienda.activo:
                tiendas_con_producto.append(tienda)
    
    # Encontrar la tienda más cercana
    tienda_cercana, distancia = encontrar_tienda_mas_cercana(tiendas_con_producto, lat, lng)
    
    if not tienda_cercana:
        return jsonify({'error': 'No se encontraron tiendas con este producto'}), 404
    
    return jsonify({
        'tienda': {
            'id': str(tienda_cercana._id),
            'nombre': tienda_cercana.nombre,
            'direccion': tienda_cercana.direccion,
            'latitud': tienda_cercana.latitud,
            'longitud': tienda_cercana.longitud,
            'distancia': round(distancia, 2)
        },
        'producto': {
            'id': str(producto._id),
            'nombre': producto.nombre,
            'precio': producto.precio
        }
    })
