from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app import mongo, login_manager
from bson import ObjectId

auth = Blueprint('auth', __name__)

class User(UserMixin):
    def __init__(self, user_data):
        self.user_data = user_data
        self.id = str(user_data['_id'])
        self.username = user_data['username']
        self.email = user_data['email']
    
    @staticmethod
    def get_by_id(user_id):
        user_data = mongo.db.users.find_one({'_id': ObjectId(user_id)})
        if user_data:
            return User(user_data)
        return None
    
    @staticmethod
    def get_by_username(username):
        user_data = mongo.db.users.find_one({'username': username})
        if user_data:
            return User(user_data)
        return None
    
    @staticmethod
    def get_by_email(email):
        user_data = mongo.db.users.find_one({'email': email})
        if user_data:
            return User(user_data)
        return None

@login_manager.user_loader
def load_user(user_id):
    return User.get_by_id(user_id)

@auth.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Validaciones
        if not username or not email or not password:
            flash('Todos los campos son obligatorios', 'danger')
            return render_template('auth/registro.html')
        
        if password != password_confirm:
            flash('Las contraseñas no coinciden', 'danger')
            return render_template('auth/registro.html')
        
        # Verificar si el usuario ya existe
        if User.get_by_username(username):
            flash('El nombre de usuario ya está en uso', 'danger')
            return render_template('auth/registro.html')
        
        if User.get_by_email(email):
            flash('El correo electrónico ya está registrado', 'danger')
            return render_template('auth/registro.html')
        
        # Crear nuevo usuario
        hashed_password = generate_password_hash(password)
        user_id = mongo.db.users.insert_one({
            'username': username,
            'email': email,
            'password': hashed_password
        }).inserted_id
        
        # Iniciar sesión automáticamente
        user_data = mongo.db.users.find_one({'_id': user_id})
        user = User(user_data)
        login_user(user)
        
        flash('Registro exitoso. ¡Bienvenido!', 'success')
        return redirect(url_for('tiendas.listar_tiendas'))
    
    return render_template('auth/registro.html')

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Validaciones
        if not username or not password:
            flash('Por favor ingresa nombre de usuario y contraseña', 'danger')
            return render_template('auth/login.html')
        
        # Buscar usuario
        user = User.get_by_username(username)
        if not user or not check_password_hash(user.user_data['password'], password):
            flash('Nombre de usuario o contraseña incorrectos', 'danger')
            return render_template('auth/login.html')
        
        # Iniciar sesión
        login_user(user)
        flash('Inicio de sesión exitoso', 'success')
        
        # Redireccionar a la página solicitada originalmente o a la lista de tiendas
        next_page = request.args.get('next')
        if next_page:
            return redirect(next_page)
        return redirect(url_for('tiendas.listar_tiendas'))
    
    return render_template('auth/login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Has cerrado sesión correctamente', 'success')
    return redirect(url_for('auth.login'))
