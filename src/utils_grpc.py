import grpc
import logging
from .utils_divipola import normalizar_texto
from . import ConsultarRegionAdministrativa_pb2 as region_pb2
from . import ConsultarRegionAdministrativa_pb2_grpc as region_pb2_grpc
from .config import GRPC_SERVER_URL

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def obtener_codigos_divipola_grpc(nombre_departamento: str, nombre_municipio: str) -> dict:
    
    dep_norm = normalizar_texto(nombre_departamento)
    mun_norm = normalizar_texto(nombre_municipio)
    mun_grpc_format = mun_norm.replace(" ", "_")
    
    if not dep_norm or not mun_norm:
        return {
            "estado": "SKIPPED",
            "error_detalle": "Faltan datos de Depto/Municipio",
            "cod_dep": None,
            "cod_mun": None,
        }

    try:
        with grpc.insecure_channel(GRPC_SERVER_URL) as channel:
            stub = region_pb2_grpc.ConsultarRegionAdministrativaServiceStub(channel)
            
            request = region_pb2.GetCodigoRegionRequest(
                nombreDepartamento=dep_norm,
                nombreMunicipio=mun_grpc_format
            )
            
            response = stub.GetCodigoRegion(request, timeout=10) 
            
            return {
                "estado": "OK",
                "error_detalle": None,
                "cod_dep": response.codigoDepartamento,
                "cod_mun": response.codigoMunicipio,
            }

    except grpc.RpcError as e:
        error_msg = f"RPC_ERROR (Code {e.code().value[0]}): {e.details()}"
        logging.error(f"Error gRPC al consultar {dep_norm}/{mun_norm}: {error_msg}")
        return {
            "estado": "RPC_FAILED",
            "error_detalle": error_msg,
            "cod_dep": None,
            "cod_mun": None,
        }
    except Exception as e:
        error_msg = f"UNEXPECTED_ERROR: {e}"
        logging.error(f"Error inesperado al conectar con gRPC: {error_msg}")
        return {
            "estado": "UNEXPECTED_FAILED",
            "error_detalle": error_msg,
            "cod_dep": None,
            "cod_mun": None,
        }