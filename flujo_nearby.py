import pandas as pd
from time import sleep

from utils_divipola import obtener_coordenadas_por_municipios
from nearby import buscar_lugares_cercanos, extraer_dep_muni

def obtener_lugares_por_municipios(df_divipola: pd.DataFrame, max_results: int = 10):
    
    municipios = obtener_coordenadas_por_municipios(df_divipola)
    resultados = []

    for i, mun in enumerate(municipios, start=1):
        lat = mun["latitud"]
        lon = mun["longitud"]

        places = buscar_lugares_cercanos(lat, lon, max_results)

        if not places:
            resultados.append({
                "codigo_departamento": mun["codigo_departamento"],
                "nombre_departamento": mun["nombre_departamento"],
                "codigo_municipio": mun["codigo_municipio"],
                "nombre_municipio": mun["nombre_municipio"],
                "lat_municipio": lat,
                "lon_municipio": lon,
                "place:name": None,
                "place:lat": None,
                "place:lon": None,
                "dep_nearby": None,
                "mun_nearby": None,
            })
            continue

        for place in places:
            location = place.get("location", {})
            dep_nearby, mun_nearby = extraer_dep_muni(place)

            resultados.append({
                "codigo_departamento": mun["codigo_departamento"],
                "nombre_departamento": mun["nombre_departamento"],
                "codigo_municipio": mun["codigo_municipio"],
                "nombre_municipio": mun["nombre_municipio"],
                "lat_municipio": lat,
                "lon_municipio": lon,
                "place:name": place.get("displayName", {}).get("text"),
                "place:lat": location.get("latitude"),
                "place:lon": location.get("longitude"),
                "dep_nearby": dep_nearby,
                "mun_nearby": mun_nearby,
            })

        sleep(0.1) 

    return resultados
        