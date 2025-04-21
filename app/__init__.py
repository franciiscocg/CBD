from flask import Flask, redirect, url_for
from flask_pymongo import PyMongo
from flask_login import LoginManager
from app.config import Config

mongo = PyMongo()
login_manager = LoginManager()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensiones
    mongo.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    
    # Crear índices geoespaciales
    with app.app_context():
        mongo.db.tiendas.create_index([("ubicacion", "2dsphere")])
    
    # Registrar blueprints
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.routes.tiendas import tiendas as tiendas_blueprint
    app.register_blueprint(tiendas_blueprint)
    
    from app.routes.productos import productos as productos_blueprint
    app.register_blueprint(productos_blueprint)
    
    from app.routes.busqueda import busqueda as busqueda_blueprint
    app.register_blueprint(busqueda_blueprint)
    
    # Ruta principal directamente en la aplicación (como respaldo)
    @app.route('/')
    def index():
        return redirect(url_for('busqueda.buscar'))
    
    return app
