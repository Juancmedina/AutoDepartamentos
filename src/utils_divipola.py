import pandas as pd
import unicodedata

RUTA_DIVIPOLA = "data/DIVIPOLA.xlsx"

def normalizar_texto(texto: str) -> str:
   
    if not isinstance(texto, str):
        return ""
    nfkd = unicodedata.normalize("NFKD", texto)
    solo_ascii = "".join([c for c in nfkd if not unicodedata.combining(c)])
    return solo_ascii.upper().strip()

def cargar_divipola(ruta: str) -> pd.DataFrame:
    
    df = pd.read_excel(ruta)

    df["Departamento_Normalizado"] = df["Nombre Departamento"].apply(normalizar_texto)
    df["Municipio_Normalizado"] = df["Nombre Municipio"].apply(normalizar_texto)

    df["Latitud_num"] = pd.to_numeric(df["Latitud"], errors="coerce")
    df["Longitud_num"] = pd.to_numeric(df["longitud"], errors="coerce")

    return df

def obtener_coordenadas_por_municipios(df_divipola: pd.DataFrame):
    
    municipios = []

    for _, fila in df_divipola.iterrows():
        municipios.append({
            "codigo_departamento": int(fila["Código Departamento"]),
            "nombre_departamento": fila["Nombre Departamento"],
            "codigo_municipio": int(fila["Código Municipio"]),
            "nombre_municipio": fila["Nombre Municipio"],
            "latitud": float(fila["Latitud_num"]),
            "longitud": float(fila["Longitud_num"]),
        })

    return municipios



def buscar_en_divipola(df_divipola: pd.DataFrame,
                       depto_google: str,
                       muni_google: str) -> dict | None:
    
    dep_norm = normalizar_texto(depto_google)
    muni_norm = normalizar_texto(muni_google)

    coincidencias = df_divipola[
        (df_divipola["Departamento_Normalizado"] == dep_norm) &
        (df_divipola["Municipio_Normalizado"] == muni_norm)
    ]

    if coincidencias.empty:
        print("No se encontró coincidencia en DIVIPOLA para:",
              depto_google, "/", muni_google)
        return None

    fila = coincidencias.iloc[0]


    return {
        "codigo_departamento": int(fila["Código Departamento"]),
        "nombre_departamento": fila["Nombre Departamento"],
        "codigo_municipio": int(fila["Código Municipio"]),
        "nombre_municipio": fila["Nombre Municipio"],
        "latitud_divipola": fila["Latitud_num"],
        "longitud_divipola": fila["Longitud_num"],
    }








