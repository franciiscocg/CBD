# Solución a problemas de dependencias en TiendasGeo

## Problema de incompatibilidad NumPy-Pandas

Si encuentras el siguiente error al ejecutar el proyecto:
```
ValueError: numpy.dtype size changed, may indicate binary incompatibility. Expected 96 from C header, got 88 from PyObject
```

Este es un problema común de incompatibilidad entre las versiones compiladas de NumPy y pandas, especialmente en entornos Windows.

## Soluciones

### Solución 1: Reinstalar en orden correcto

```bash
# Desinstalar ambos paquetes
pip uninstall numpy pandas -y

# Instalar primero NumPy con versión específica
pip install numpy==1.24.3

# Luego instalar pandas
pip install pandas==2.0.3
```

### Solución 2: Forzar reinstalación de todas las dependencias

```bash
pip install -r requirements.txt --force-reinstall
```

### Solución 3: Crear un nuevo entorno virtual

```bash
# Crear nuevo entorno
python -m venv new_venv

# Activar (Windows)
new_venv\Scripts\activate

# Activar (Linux/Mac)
source new_venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## Versiones compatibles recomendadas

Para este proyecto, recomendamos las siguientes versiones de paquetes:

- Python: 3.10.x
- NumPy: 1.24.3
- pandas: 2.0.3
- Flask: 2.3.3
- PyMongo: 4.5.0

## Problemas adicionales

Si encuentras otros problemas de dependencias, por favor consulta la documentación oficial o contacta al equipo de desarrollo.
