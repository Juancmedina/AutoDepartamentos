import pandas as pd
from flujo_nearby import obtener_lugares_por_municipios
from utils_divipola import (
    cargar_divipola,
    obtener_coordenadas_por_municipios,
    buscar_en_divipola,
    RUTA_DIVIPOLA
)


def main():

    df_divipola = cargar_divipola(RUTA_DIVIPOLA)
    print(f"Se cargaron {len(df_divipola)} registros de DIVIPOLA.")
    
    
    MODO_PRUEBA = True           # pon False para correr todo
    NUM_MUNICIPIOS_PRUEBA = 2    

    if MODO_PRUEBA:
        df_entrada = df_divipola.head(NUM_MUNICIPIOS_PRUEBA)
        nombre_salida = "nearby_por_municipio_PRUEBA.xlsx"
        print(f"Ejecutando en modo prueba con {len(df_entrada)} municipios...")
    else:
        df_entrada = df_divipola
        nombre_salida = "nearby_por_municipio_FULL.xlsx"
        print("Ejecutando para TODOS los municipios...")

    resultados = obtener_lugares_por_municipios(df_entrada, max_results=10)
    print(f"Total de filas generadas: {len(resultados)}")

    df_resultados = pd.DataFrame(resultados)
    df_resultados.to_excel(nombre_salida, index=False)

    print(f"Archivo generado: {nombre_salida}")


if __name__ == "__main__":
    main()

