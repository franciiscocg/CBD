# Presentación: TiendasGeo

## Diapositiva 1: Portada
- **Título:** TiendasGeo - Aplicación de Búsqueda de Productos Cercanos
- **Subtítulo:** Solución geoespacial con MongoDB y Flask
- **Fecha:** Abril 2025

## Diapositiva 2: Problema y Solución
- **Problema:**
  - Dificultad para encontrar productos específicos en tiendas cercanas
  - Falta de herramientas para que pequeños comercios gestionen su inventario
  - Necesidad de integración de datos geoespaciales con inventarios de productos

- **Solución:**
  - Aplicación web que conecta usuarios con tiendas cercanas
  - Sistema de gestión de inventario con carga CSV para comerciantes
  - Búsqueda geoespacial para encontrar la tienda más cercana con el producto deseado

## Diapositiva 3: Tecnologías Utilizadas
- **Backend:**
  - Flask: Framework web ligero y flexible
  - PyMongo: Integración directa con MongoDB
  - Servicios geoespaciales nativos

- **Base de Datos:**
  - MongoDB: Base de datos NoSQL con capacidades geoespaciales nativas
  - Índices 2dsphere para consultas de proximidad eficientes

- **Frontend:**
  - Bootstrap 5: Diseño responsive
  - Leaflet.js: Mapas interactivos
  - JavaScript: Interactividad y geolocalización

## Diapositiva 4: Arquitectura del Sistema
- **Diagrama de Arquitectura:**
  - Capa de presentación (HTML, CSS, JS)
  - Capa de aplicación (Flask, Blueprints)
  - Capa de servicios (Geo, CSV)
  - Capa de datos (MongoDB)

- **Ventajas:**
  - Desacoplamiento de componentes
  - Escalabilidad horizontal
  - Mantenibilidad y testabilidad

## Diapositiva 5: Modelo de Datos
- **Colecciones principales:**
  - Usuarios: Autenticación y perfiles
  - Tiendas: Información y ubicación geoespacial
  - Productos: Inventario y disponibilidad

- **Características:**
  - Esquema flexible
  - Soporte nativo para datos geoespaciales
  - Índices optimizados para búsquedas

## Diapositiva 6: Funcionalidades Principales
- **Para Usuarios:**
  - Búsqueda de productos
  - Localización de tiendas cercanas
  - Visualización en mapas interactivos

- **Para Comerciantes:**
  - Gestión de tiendas y ubicaciones
  - Administración de inventario
  - Carga masiva de productos vía CSV

## Diapositiva 7: Búsqueda Geoespacial
- **Características:**
  - Utiliza índices 2dsphere de MongoDB
  - Cálculo de distancias con fórmula de Haversine
  - Filtrado por radio de búsqueda

- **Ejemplo de consulta:**
  ```python
  tiendas_cercanas = Tienda.find_near(lat, lng, radio_metros, {'activo': True})
  ```

## Diapositiva 8: Carga de Productos CSV
- **Proceso:**
  - Validación de formato y columnas requeridas
  - Procesamiento fila por fila
  - Creación o actualización de productos existentes

- **Ventajas:**
  - Importación masiva eficiente
  - Compatible con sistemas de gestión de inventario
  - Validación y manejo de errores

## Diapositiva 9: Interfaz de Usuario
- **Características:**
  - Diseño responsive para móviles y escritorio
  - Mapas interactivos con Leaflet.js
  - Geolocalización del usuario
  - Formularios intuitivos para gestión

- **Demostración:**
  - Capturas de pantalla de las principales interfaces

## Diapositiva 10: Despliegue
- **Opciones de despliegue:**
  - Entorno de desarrollo local
  - Contenedores Docker
  - Servicios en la nube

- **Requisitos:**
  - Python 3.10+
  - MongoDB 4.4+
  - Navegador moderno con soporte para geolocalización

## Diapositiva 11: Pruebas y Calidad
- **Estrategia de pruebas:**
  - Pruebas unitarias con Pytest
  - Pruebas de integración
  - Validación de funcionalidades geoespaciales

- **Métricas:**
  - Cobertura de código
  - Tiempo de respuesta
  - Precisión de búsquedas geoespaciales

## Diapositiva 12: Demostración
- **Escenarios de demostración:**
  1. Registro de usuario y creación de tienda
  2. Carga de productos desde CSV
  3. Búsqueda de productos cercanos
  4. Visualización en mapa interactivo

## Diapositiva 13: Ventajas de la Arquitectura
- **Comparación con soluciones alternativas:**
  - Django + Djongo vs Flask + PyMongo
  - Ventajas de la integración directa con MongoDB
  - Mejor rendimiento en operaciones geoespaciales
  - Mayor flexibilidad y mantenibilidad

## Diapositiva 14: Trabajo Futuro
- **Próximos pasos:**
  - API REST para integración con aplicaciones móviles
  - Análisis de datos y recomendaciones personalizadas
  - Integración con servicios de navegación y rutas
  - Escalabilidad para grandes volúmenes de datos

## Diapositiva 15: Conclusiones
- **Logros:**
  - Implementación exitosa de funcionalidades geoespaciales
  - Solución eficiente para la gestión de inventario
  - Interfaz intuitiva para usuarios y comerciantes

- **Lecciones aprendidas:**
  - Importancia de elegir las tecnologías adecuadas
  - Ventajas de MongoDB para datos geoespaciales
  - Flexibilidad de Flask para aplicaciones modulares

## Diapositiva 16: Preguntas y Respuestas
- **Contacto:**
  - Información de contacto
  - Repositorio del proyecto
  - Documentación adicional
