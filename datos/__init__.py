# Capa de datos: contiene los repositorios para leer los archivos JSON.
# Permite consultar productos y las normas de transito de forma organizada.

from datos.producto_repository import ProductoRepository
from datos.traffic_code_repository import TrafficCodeRepository

# Lista de clases disponibles para usar en otras partes del proyecto.
__all__ = ["ProductoRepository", "TrafficCodeRepository"]
