import json
import requests
import pandas as pd

from utils_divipola import (
    cargar_divipola,
    buscar_en_divipola,
    RUTA_DIVIPOLA
)

API_KEY = "AIzaSyBep8722UIKODElaxjOCPXjlUr85zS8rzI" 
BASE_URL = "https://maps.googleapis.com/maps/api/geocode/json"

LATITUD = 8.882597
LONGITUD = -75.797453

def obtener_departamento_y_municipio_de_api(lat: float, lon: float) -> tuple[str  | None, str | None]:

    params = {
        'latlng': f"{lat},{lon}",
        'key': API_KEY,
    }
    
    print(f"   🌍 Consultando API para Latitud: {lat}, Longitud: {lon}...")
    
    try:
        response = requests.get(BASE_URL, params=params)
        response.raise_for_status()
        data = response.json()
        nombre_departamento = None
        nombre_municipio = None
        
        if data.get('status') == 'OK' and data.get('results'):
            address_components = data['results'][0].get('address_components', [])

            for component in address_components:
                types = component.get('types', [])
                long_name = component.get('long_name')

                if not long_name:
                    continue


                if 'administrative_area_level_1' in types:
                    nombre_departamento = long_name
                    print(f"   ✅ Nombre del Departamento obtenido: {nombre_departamento}")

                elif 'administrative_area_level_2' in types:
                    nombre_municipio = long_name
                    print(f"   ✅ Nombre del Municipio obtenido: {nombre_municipio}")

                if nombre_departamento and nombre_municipio:
                    break

            if nombre_departamento and nombre_municipio:
                    return nombre_departamento, nombre_municipio
                
        print("   ❌ Error: La API no pudo encontrar el departamento o el JSON no tiene el formato esperado.")
        return None, None
        
    except requests.exceptions.RequestException as e:
        print(f"   ❌ Error al conectar con la API: {e}")
        return None, None
    
if __name__ == "__main__":
    
    departamento, municipio = obtener_departamento_y_municipio_de_api(LATITUD, LONGITUD)

    df_divipola = cargar_divipola(RUTA_DIVIPOLA)
    print("\n Buscando coincidencia en DIVIPOLA..")
    info_divipola = buscar_en_divipola(df_divipola, departamento, municipio)
    print(f"   ✅ Resultado en DIVIPOLA:")
    print(json.dumps(info_divipola, indent=4, ensure_ascii=False))