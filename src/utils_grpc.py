import grpc
import logging

from .import ConsultarRegionAdministrativa_pb2 as region_pb2
from .import ConsultarRegionAdministrativa_pb2_grpc as region_pb2_grpc
from .config import GRPC_SERVER_URL

logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')

def obtener_codigos_divipola_grpc(nombre_departamento: str, nombre_municipio: str) -> tuple[str, str] | tuple[None, None]:
    """
    Llama al servicio gRPC para obtener el código DIVIPOLA 
    a partir del nombre del departamento y municipio.
    """
    
    dep_norm = nombre_departamento.upper().strip() if nombre_departamento else ""
    mun_norm = nombre_municipio.upper().strip() if nombre_municipio else ""

    mun_grpc_format = mun_norm.replace(" ", "_")
    
    if not dep_norm or not mun_norm:
        return None, None

    try:
        with grpc.insecure_channel(GRPC_SERVER_URL) as channel:
            stub = region_pb2_grpc.ConsultarRegionAdministrativaServiceStub(channel)
            
            request = region_pb2.GetCodigoRegionRequest(
                nombreDepartamento=dep_norm,
                nombreMunicipio=mun_grpc_format
            )
            
            response = stub.GetCodigoRegion(request, timeout=10) 
            
            return response.codigoDepartamento, response.codigoMunicipio

    except grpc.RpcError as e:
        logging.error(f"Error gRPC al consultar {dep_norm}/{mun_norm}: Código {e.code().value[0]} - Detalles: {e.details()}")
        return None, None
    except Exception as e:
        logging.error(f"Error inesperado al conectar con gRPC: {e}")
        return None, None