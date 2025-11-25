import requests
from config import PLACES_API_KEY

PLACES_URL = "https://places.googleapis.com/v1/places:searchNearby"

def buscar_lugares_cercanos(lat: float, lon: float, max_results: int = 10):
  
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

#PREGUNTAR

def extraer_dep_muni(place):
    
    departamento = None
    municipio = None

    for comp in place.get("addressComponents", []):
        types = comp.get("types", [])

        if "administrative_area_level_1" in types:
            departamento = comp.get("longText")

        if "administrative_area_level_2" in types:
            municipio = comp.get("longText")

    return departamento, municipio








