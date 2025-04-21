# Manual de Usuario - TiendasGeo

## Índice

1. [Introducción](#1-introducción)
2. [Acceso a la Aplicación](#2-acceso-a-la-aplicación)
3. [Registro e Inicio de Sesión](#3-registro-e-inicio-de-sesión)
4. [Búsqueda de Productos](#4-búsqueda-de-productos)
5. [Visualización de Mapas](#5-visualización-de-mapas)
6. [Gestión de Tiendas](#6-gestión-de-tiendas)
7. [Gestión de Productos](#7-gestión-de-productos)
8. [Carga de Productos desde CSV](#8-carga-de-productos-desde-csv)
9. [Preguntas Frecuentes](#9-preguntas-frecuentes)

## 1. Introducción

TiendasGeo es una aplicación web que te permite buscar productos y encontrar la tienda más cercana donde están disponibles. Si eres dueño de una tienda, también puedes registrar tu negocio, añadir productos y gestionar tu inventario.

## 2. Acceso a la Aplicación

Para acceder a TiendasGeo, abre tu navegador web y visita la dirección proporcionada por el administrador del sistema (por ejemplo, http://localhost:5000 en entorno local).

La aplicación es compatible con los siguientes navegadores:
- Google Chrome (recomendado)
- Mozilla Firefox
- Microsoft Edge
- Safari

## 3. Registro e Inicio de Sesión

### 3.1 Registro de Usuario

1. Haz clic en "Registrarse" en la barra de navegación superior.
2. Completa el formulario con tu nombre de usuario, correo electrónico y contraseña.
3. Haz clic en el botón "Registrarse".
4. Una vez registrado, serás redirigido automáticamente a la página principal.

### 3.2 Inicio de Sesión

1. Haz clic en "Iniciar Sesión" en la barra de navegación superior.
2. Introduce tu nombre de usuario y contraseña.
3. Haz clic en el botón "Iniciar Sesión".

### 3.3 Cierre de Sesión

1. Haz clic en tu nombre de usuario en la barra de navegación superior.
2. Selecciona "Cerrar Sesión" en el menú desplegable.

## 4. Búsqueda de Productos

### 4.1 Búsqueda Básica

1. En la página principal, introduce el nombre del producto que buscas en la barra de búsqueda.
2. Haz clic en el botón "Buscar" o presiona Enter.
3. Se mostrarán los resultados de la búsqueda.

### 4.2 Búsqueda con Ubicación

Para encontrar la tienda más cercana con el producto que buscas:

1. Introduce el nombre del producto en la barra de búsqueda.
2. Haz clic en el botón de ubicación (icono de marcador) para activar tu ubicación.
3. Cuando se detecte tu ubicación, haz clic en "Buscar".
4. Los resultados mostrarán la tienda más cercana que tiene el producto, junto con la distancia.

## 5. Visualización de Mapas

### 5.1 Mapa de Búsqueda

1. Accede a la página "Mapa" desde la barra de navegación.
2. El mapa mostrará todas las tiendas registradas.
3. Puedes hacer zoom y desplazarte por el mapa.
4. Haz clic en los marcadores para ver información detallada de cada tienda.

### 5.2 Activar tu Ubicación

1. Haz clic en el botón de ubicación (icono de marcador).
2. Permite el acceso a tu ubicación cuando el navegador lo solicite.
3. Tu posición se mostrará en el mapa con un marcador azul.
4. Las tiendas cercanas se mostrarán con marcadores rojos.

## 6. Gestión de Tiendas

### 6.1 Ver Mis Tiendas

1. Inicia sesión en tu cuenta.
2. Haz clic en tu nombre de usuario en la barra de navegación.
3. Selecciona "Mis Tiendas" en el menú desplegable.
4. Verás una lista de todas tus tiendas registradas.

### 6.2 Crear Nueva Tienda

1. En la página "Mis Tiendas", haz clic en el botón "Nueva Tienda".
2. Completa el formulario con la información de tu tienda:
   - Nombre de la tienda (obligatorio)
   - Descripción
   - Dirección (obligatorio)
   - Teléfono
   - Email
   - Sitio web
   - Horario
   - Categorías (separadas por comas)
3. Selecciona la ubicación de tu tienda en el mapa:
   - Puedes buscar una dirección y hacer clic en "Buscar"
   - O hacer clic directamente en el mapa
   - Las coordenadas se completarán automáticamente
4. Haz clic en "Guardar Tienda".

### 6.3 Editar Tienda

1. En la página "Mis Tiendas", haz clic en el botón "Editar" de la tienda que deseas modificar.
2. Actualiza la información necesaria.
3. Haz clic en "Guardar Cambios".

### 6.4 Ver Detalles de Tienda

1. En la página "Mis Tiendas", haz clic en el botón "Ver" de la tienda.
2. Verás los detalles completos de la tienda y sus productos.

## 7. Gestión de Productos

### 7.1 Ver Productos de una Tienda

1. En la página "Mis Tiendas", haz clic en el botón "Productos" de la tienda.
2. Verás una lista de todos los productos de esa tienda.

### 7.2 Añadir Nuevo Producto

1. En la página de productos de la tienda, haz clic en "Nuevo Producto".
2. Completa el formulario con la información del producto:
   - Nombre (obligatorio)
   - Descripción
   - Código
   - Precio (obligatorio)
   - Stock (obligatorio)
   - Categoría
   - Imagen (opcional)
3. Haz clic en "Guardar Producto".

### 7.3 Editar Producto

1. En la lista de productos, haz clic en el botón "Editar" del producto que deseas modificar.
2. Actualiza la información necesaria.
3. Haz clic en "Guardar Cambios".

### 7.4 Eliminar Producto

1. En la lista de productos, haz clic en el botón "Eliminar" del producto.
2. Confirma la eliminación en el cuadro de diálogo.

## 8. Carga de Productos desde CSV

### 8.1 Preparar Archivo CSV

Crea un archivo CSV con las siguientes columnas:
- `nombre` (obligatorio): Nombre del producto
- `precio` (obligatorio): Precio del producto (número decimal)
- `stock` (obligatorio): Cantidad disponible (número entero)
- `descripcion` (opcional): Descripción del producto
- `codigo` (opcional): Código o referencia del producto
- `categoria` (opcional): Categoría del producto

Ejemplo:
```
nombre,precio,stock,descripcion,codigo,categoria
Smartphone XYZ,299.99,10,Smartphone de última generación,SM001,Electrónica
Auriculares Bluetooth,49.99,20,Auriculares inalámbricos con cancelación de ruido,AU002,Accesorios
```

### 8.2 Cargar Archivo CSV

1. En la página de productos de la tienda, haz clic en "Cargar CSV".
2. Haz clic en "Seleccionar archivo" y elige tu archivo CSV.
3. Haz clic en "Cargar Archivo".
4. Se mostrará un resumen con el número de productos creados, actualizados y errores.

## 9. Preguntas Frecuentes

### ¿Cómo se calcula la tienda más cercana?

La aplicación utiliza tu ubicación geográfica (latitud y longitud) y calcula la distancia a cada tienda utilizando la fórmula de Haversine, que tiene en cuenta la curvatura de la Tierra.

### ¿Por qué necesito activar mi ubicación?

Para encontrar la tienda más cercana con el producto que buscas, la aplicación necesita conocer tu ubicación actual. Esta información solo se utiliza para calcular distancias y no se almacena en nuestros servidores.

### ¿Qué hago si no aparecen mis productos después de cargar el CSV?

Verifica que tu archivo CSV tenga el formato correcto y contenga todas las columnas obligatorias (nombre, precio, stock). Si el problema persiste, intenta cargar los productos individualmente.

### ¿Puedo tener múltiples tiendas con mi cuenta?

Sí, puedes crear y gestionar tantas tiendas como necesites con una sola cuenta de usuario.

### ¿Cómo actualizo el stock de mis productos?

Puedes actualizar el stock de tus productos de dos formas:
1. Editando cada producto individualmente
2. Cargando un nuevo archivo CSV con los valores actualizados (los productos existentes se actualizarán automáticamente si tienen el mismo código o nombre)
