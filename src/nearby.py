import requests
from .config import PLACES_API_KEY 

PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"

def buscar_lugares_cercanos(lat: float, lon: float, max_results: int = 5):
  
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": PLACES_API_KEY,
        "X-Goog-FieldMask": "places.id,places.displayName,places.location,places.addressComponents"
    }

    body = {
        "includedTypes": ["store"],
        "maxResultCount": max_results,
        "locationRestriction": {
            "circle": {
                "center": {
                    "latitude": lat,
                    "longitude": lon
                },
                "radius": 2000.0  # metros
            }
        }
    }

    response = requests.post(PLACES_URL, headers=headers, json=body)
    response.raise_for_status()
    data = response.json()
    return data.get('places', [])

def extraer_dep_muni(place):
    
    departamento = None
    municipio_principal = None
    municipio_localidad = None 

    for comp in place.get("addressComponents", []):
        types = comp.get("types", [])
        long_name = comp.get("longText")

        if not long_name:
            continue

        if "administrative_area_level_1" in types and departamento is None:
            departamento = long_name

        if "administrative_area_level_2" in types and municipio_principal is None:
            municipio_principal = long_name
        
        if "locality" in types and municipio_localidad is None:
            municipio_localidad = long_name

    return departamento, municipio_principal, municipio_localidad