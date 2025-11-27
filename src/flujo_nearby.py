import pandas as pd
from time import sleep

from .utils_divipola import obtener_coordenadas_por_municipios
from .nearby import buscar_lugares_cercanos, extraer_dep_muni
from .utils_grpc import obtener_codigos_divipola_grpc

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
                "cod_dep_nearby_GRPC": None,
                "cod_mun_nearby_GRPC": None, 
                "DIVIPOLA_GRPC_COINCIDE": False,
            })
            continue

        for place in places:
            location = place.get("location", {})
            
            dep_nearby_nombre, mun_nearby_nombre = extraer_dep_muni(place) 

            cod_dep_nearby_grpc, cod_mun_nearby_grpc = obtener_codigos_divipola_grpc(
                dep_nearby_nombre, mun_nearby_nombre
            )

            cod_dep_municipio_central = str(mun["codigo_departamento"])
            cod_mun_municipio_central = str(mun["codigo_municipio"])

            dep_central_formato = cod_dep_municipio_central.zfill(2)
            mun_central_formato = cod_mun_municipio_central.zfill(5)

            codigos_coinciden = (cod_dep_nearby_grpc == dep_central_formato) and \
                                (cod_mun_nearby_grpc == mun_central_formato)
            
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
                "dep_nearby": dep_nearby_nombre,    
                "mun_nearby": mun_nearby_nombre,       
                "cod_dep_nearby_GRPC": cod_dep_nearby_grpc,
                "cod_mun_nearby_GRPC": cod_mun_nearby_grpc,
                "DIVIPOLA_GRPC_COINCIDE": codigos_coinciden
            })

        sleep(0.1) 

    return resultados