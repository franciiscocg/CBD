from flask import Blueprint, render_template, request, redirect, url_for, flash, current_app
from flask_login import login_required, current_user
from werkzeug.utils import secure_filename
import os
from app.models.tienda import Tienda
from app.models.producto import Producto
from app.services.csv_service import procesar_csv
from bson import ObjectId

productos = Blueprint('productos', __name__)

@productos.route('/productos/tienda/<tienda_id>')
@login_required
def listar_productos(tienda_id):
    """Lista los productos de una tienda específica."""
    tienda = Tienda.find_by_id(tienda_id)
    
    if not tienda or str(tienda.propietario_id) != str(current_user.id):
        flash('Tienda no encontrada o no tienes permiso para ver esta tienda', 'danger')
        return redirect(url_for('tiendas.listar_tiendas'))
    
    productos_lista = Producto.find_by_tienda(ObjectId(tienda_id))
    
    return render_template('productos/listar.html', 
                          tienda=tienda, 
                          productos=productos_lista)

@productos.route('/productos/crear/<tienda_id>', methods=['GET', 'POST'])
@login_required
def crear_producto(tienda_id):
    """Crea un nuevo producto para una tienda específica."""
    tienda = Tienda.find_by_id(tienda_id)
    
    if not tienda or str(tienda.propietario_id) != str(current_user.id):
        flash('Tienda no encontrada o no tienes permiso para modificar esta tienda', 'danger')
        return redirect(url_for('tiendas.listar_tiendas'))
    
    if request.method == 'POST':
        nombre = request.form.get('nombre')
        descripcion = request.form.get('descripcion')
        codigo = request.form.get('codigo')
        precio = float(request.form.get('precio'))
        stock = int(request.form.get('stock'))
        categoria = request.form.get('categoria')
        
        # Manejar imagen si se proporciona
        imagen = None
        if 'imagen' in request.files and request.files['imagen'].filename:
            file = request.files['imagen']
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            imagen = '/static/uploads/' + filename
        
        producto = Producto(
            nombre=nombre,
            descripcion=descripcion,
            codigo=codigo,
            precio=precio,
            stock=stock,
            tienda_id=ObjectId(tienda_id),
            categoria=categoria,
            imagen=imagen
        )
        
        producto.save()
        flash('Producto creado correctamente', 'success')
        return redirect(url_for('productos.listar_productos', tienda_id=tienda_id))
    
    return render_template('productos/crear.html', tienda=tienda)

@productos.route('/productos/editar/<producto_id>', methods=['GET', 'POST'])
@login_required
def editar_producto(producto_id):
    """Edita un producto existente."""
    producto = Producto.find_by_id(producto_id)
    
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('tiendas.listar_tiendas'))
    
    tienda = Tienda.find_by_id(producto.tienda_id)
    
    if not tienda or str(tienda.propietario_id) != str(current_user.id):
        flash('No tienes permiso para modificar este producto', 'danger')
        return redirect(url_for('tiendas.listar_tiendas'))
    
    if request.method == 'POST':
        producto.nombre = request.form.get('nombre')
        producto.descripcion = request.form.get('descripcion')
        producto.codigo = request.form.get('codigo')
        producto.precio = float(request.form.get('precio'))
        producto.stock = int(request.form.get('stock'))
        producto.categoria = request.form.get('categoria')
        
        # Manejar imagen si se proporciona
        if 'imagen' in request.files and request.files['imagen'].filename:
            file = request.files['imagen']
            filename = secure_filename(file.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            os.makedirs(upload_folder, exist_ok=True)
            file_path = os.path.join(upload_folder, filename)
            file.save(file_path)
            producto.imagen = '/static/uploads/' + filename
        
        producto.save()
        flash('Producto actualizado correctamente', 'success')
        return redirect(url_for('productos.listar_productos', tienda_id=str(tienda._id)))
    
    return render_template('productos/editar.html', producto=producto, tienda=tienda)

@productos.route('/productos/eliminar/<producto_id>', methods=['POST'])
@login_required
def eliminar_producto(producto_id):
    """Elimina un producto existente."""
    producto = Producto.find_by_id(producto_id)
    
    if not producto:
        flash('Producto no encontrado', 'danger')
        return redirect(url_for('tiendas.listar_tiendas'))
    
    tienda = Tienda.find_by_id(producto.tienda_id)
    
    if not tienda or str(tienda.propietario_id) != str(current_user.id):
        flash('No tienes permiso para eliminar este producto', 'danger')
        return redirect(url_for('tiendas.listar_tiendas'))
    
    # Guardar el ID de la tienda antes de eliminar el producto
    tienda_id = str(producto.tienda_id)
    
    # Eliminar el producto
    producto.delete()
    
    flash('Producto eliminado correctamente', 'success')
    return redirect(url_for('productos.listar_productos', tienda_id=tienda_id))

@productos.route('/productos/cargar-csv/<tienda_id>', methods=['GET', 'POST'])
@login_required
def cargar_csv(tienda_id):
    """Carga productos desde un archivo CSV."""
    tienda = Tienda.find_by_id(tienda_id)
    
    if not tienda or str(tienda.propietario_id) != str(current_user.id):
        flash('Tienda no encontrada o no tienes permiso para modificar esta tienda', 'danger')
        return redirect(url_for('tiendas.listar_tiendas'))
    
    if request.method == 'POST':
        if 'archivo_csv' not in request.files:
            flash('No se ha seleccionado ningún archivo', 'danger')
            return redirect(request.url)
        
        file = request.files['archivo_csv']
        
        if file.filename == '':
            flash('No se ha seleccionado ningún archivo', 'danger')
            return redirect(request.url)
        
        if file and file.filename.endswith('.csv'):
            try:
                resultados = procesar_csv(file, tienda_id)
                flash(f'Archivo procesado correctamente. Productos creados: {resultados["creados"]}, actualizados: {resultados["actualizados"]}, errores: {resultados["errores"]}', 'success')
                return redirect(url_for('productos.listar_productos', tienda_id=tienda_id))
            except Exception as e:
                flash(f'Error al procesar el archivo: {str(e)}', 'danger')
                return redirect(request.url)
        else:
            flash('El archivo debe tener formato CSV', 'danger')
            return redirect(request.url)
    
    return render_template('productos/cargar_csv.html', tienda=tienda)

@productos.route('/productos/buscar')
def buscar_productos():
    """Busca productos por término de búsqueda."""
    termino = request.args.get('termino', '')
    
    if not termino:
        return render_template('productos/buscar.html', productos=[], termino='')
    
    productos_lista = Producto.search(termino)
    
    # Obtener información de tiendas para cada producto
    resultados = []
    for producto in productos_lista:
        tienda = Tienda.find_by_id(producto.tienda_id)
        if tienda and tienda.activo:
            resultados.append({
                'producto': producto,
                'tienda': tienda
            })
    
    return render_template('productos/buscar.html', 
                          resultados=resultados, 
                          termino=termino)
