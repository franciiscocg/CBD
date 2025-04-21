import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-secreta-por-defecto'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/tiendas_geo_db'
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
    MAX_CONTENT_LENGTH = 10 * 1024 * 1024  # 10 MB
