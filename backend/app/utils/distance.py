"""
Distance calculation utilities using Haversine formula
"""
import math


def haversine_distance(lat1: float, lng1: float, lat2: float, lng2: float) -> float:
    """
    Calculate the great circle distance between two points 
    on the earth (specified in decimal degrees)
    
    Returns distance in kilometers
    """
    # Earth's radius in kilometers
    R = 6371.0
    
    # Convert degrees to radians
    lat1_rad = math.radians(lat1)
    lon1_rad = math.radians(lng1)
    lat2_rad = math.radians(lat2)
    lon2_rad = math.radians(lng2)
    
    # Differences
    dlat = lat2_rad - lat1_rad
    dlon = lon2_rad - lon1_rad
    
    # Haversine formula
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1_rad) * math.cos(lat2_rad) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    distance = R * c
    
    return distance


def get_nearest_warehouse(seller_location: dict, warehouses: list) -> tuple:
    """
    Find the nearest warehouse to a seller location
    
    Args:
        seller_location: Dictionary with 'lat' and 'lng' keys
        warehouses: List of warehouse objects with location attribute
        
    Returns:
        Tuple of (warehouse, distance_km)
    """
    nearest_warehouse = None
    min_distance = float('inf')
    
    for warehouse in warehouses:
        distance = haversine_distance(
            seller_location['lat'],
            seller_location['lng'],
            warehouse.location['lat'],
            warehouse.location['lng']
        )
        
        if distance < min_distance:
            min_distance = distance
            nearest_warehouse = warehouse
    
    return nearest_warehouse, min_distance
