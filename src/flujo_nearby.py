import pandas as pd
from time import sleep

from .utils_divipola import obtener_coordenadas_por_municipios, normalizar_texto
from .nearby import buscar_lugares_cercanos, extraer_dep_muni
from .utils_grpc import obtener_codigos_divipola_grpc 


def obtener_lugares_por_municipios(df_divipola: pd.DataFrame, max_results: int = 10):
    
    municipios = obtener_coordenadas_por_municipios(df_divipola)
    resultados = []

    for i, mun in enumerate(municipios, start=1):
        lat = mun["latitud"]
        lon = mun["longitud"]
        mun_central_nombre = mun["nombre_municipio"]

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
                "mun_primary": None,                      
                "mun_locality_fallback": None,            
                "mun_final_usado_grpc": None,             
                "cod_dep_nearby_GRPC": None, 
                "cod_mun_nearby_GRPC": None, 
                "DIVIPOLA_GRPC_COINCIDE": False,
            })
            continue

        for place in places:
            location = place.get("location", {})
            
            dep_nearby_nombre, mun_primary_nombre, mun_locality_nombre = extraer_dep_muni(place) 

            cod_dep_nearby_grpc = None
            cod_mun_nearby_grpc = None
            mun_final_usado = None           
            mun_last_attempted = None 
            
            grpc_result = {"estado": "NO_ATTEMPT", "error_detalle": "No se intentó la consulta", "cod_dep": None, "cod_mun": None}

            mun_central_norm = normalizar_texto(mun_central_nombre)
            mun_primary_norm = normalizar_texto(mun_primary_nombre)
            mun_locality_norm = normalizar_texto(mun_locality_nombre)
            
            if mun_locality_nombre and (mun_locality_norm == mun_central_norm):
                attempt_names = [mun_locality_nombre, mun_primary_nombre]
            else:
                attempt_names = [mun_primary_nombre, mun_locality_nombre]

            attempt_names = list(dict.fromkeys([n for n in attempt_names if n]))

            for attempt_name in attempt_names:
                
                mun_last_attempted = attempt_name 
                
                grpc_result = obtener_codigos_divipola_grpc(dep_nearby_nombre, attempt_name)
                
                if grpc_result["estado"] == "OK":
                    cod_dep_nearby_grpc = grpc_result["cod_dep"]
                    cod_mun_nearby_grpc = grpc_result["cod_mun"]
                    mun_final_usado = attempt_name 
                    break

            final_mun_diagnosis = mun_final_usado if mun_final_usado else mun_last_attempted
            
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
                "mun_primary": mun_primary_nombre,                          
                "mun_locality_fallback": mun_locality_nombre,               
                "mun_final_usado_grpc": final_mun_diagnosis,                
                "cod_dep_nearby_GRPC": cod_dep_nearby_grpc, 
                "cod_mun_nearby_GRPC": cod_mun_nearby_grpc, 
                "DIVIPOLA_GRPC_COINCIDE": codigos_coinciden,
                "GRPC_ESTADO": grpc_result["estado"],
                "GRPC_ERROR_DETALLE": grpc_result["error_detalle"],
            })

        sleep(0.1) 

    return resultados