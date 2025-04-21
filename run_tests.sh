#!/bin/bash

# Script para ejecutar las pruebas de la aplicación

# Verificar si Python está instalado
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si pip está instalado
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 no está instalado. Por favor, instálalo antes de continuar."
    exit 1
fi

# Verificar si el entorno virtual existe, si no, crearlo
if [ ! -d "venv" ]; then
    echo "Creando entorno virtual..."
    python3 -m venv venv
fi

# Activar entorno virtual
echo "Activando entorno virtual..."
source venv/bin/activate

# Instalar dependencias
echo "Instalando dependencias..."
pip install -r requirements.txt
pip install pytest pytest-cov

# Verificar si MongoDB está en ejecución
echo "Verificando conexión a MongoDB..."
if ! command -v mongod &> /dev/null; then
    echo "Advertencia: MongoDB no parece estar instalado localmente."
    echo "Asegúrate de que MongoDB esté en ejecución en localhost:27017 o configura MONGO_URI en el archivo .env"
else
    if ! pgrep -x mongod > /dev/null; then
        echo "Advertencia: MongoDB no parece estar en ejecución."
        echo "Por favor, inicia MongoDB antes de continuar o configura MONGO_URI en el archivo .env"
    else
        echo "MongoDB está en ejecución."
    fi
fi

# Ejecutar pruebas
echo "Ejecutando pruebas..."
python -m pytest tests/ -v
