from math import radians, cos, sin, asin, sqrt

def calcular_distancia(lat1, lon1, lat2, lon2):
    """
    Calcula la distancia entre dos puntos geográficos utilizando la fórmula de Haversine.
    
    Args:
        lat1: Latitud del punto 1 en grados decimales
        lon1: Longitud del punto 1 en grados decimales
        lat2: Latitud del punto 2 en grados decimales
        lon2: Longitud del punto 2 en grados decimales
        
    Returns:
        float: Distancia en kilómetros entre los dos puntos
    """
    # Convertir coordenadas a radianes
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    
    # Fórmula de Haversine
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # Radio de la Tierra en kilómetros
    
    return c * r

def encontrar_tienda_mas_cercana(tiendas, lat, lon):
    """
    Encuentra la tienda más cercana a una ubicación dada.
    
    Args:
        tiendas: Lista de objetos Tienda
        lat: Latitud de la ubicación de referencia
        lon: Longitud de la ubicación de referencia
        
    Returns:
        tuple: (tienda_mas_cercana, distancia_en_km)
    """
    if not tiendas:
        return None, None
    
    tienda_mas_cercana = None
    distancia_minima = float('inf')
    
    for tienda in tiendas:
        distancia = calcular_distancia(lat, lon, tienda.latitud, tienda.longitud)
        if distancia < distancia_minima:
            distancia_minima = distancia
            tienda_mas_cercana = tienda
    
    return tienda_mas_cercana, distancia_minima
