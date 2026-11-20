"""
=============================================================================
CAPA DE DATOS — GarajeCOL
=============================================================================
Módulo de inicialización de la capa de datos.
Esta capa es responsable exclusivamente del acceso y persistencia de
información desde las fuentes de almacenamiento (archivos JSON).

Contiene los repositorios:
  - ProductoRepository: Acceso y mapeo de productos a objetos de dominio.
  - TrafficCodeRepository: Acceso a la normativa del Código de Tránsito.
=============================================================================
"""

from datos.producto_repository import ProductoRepository
from datos.traffic_code_repository import TrafficCodeRepository

__all__ = [
    "ProductoRepository",
    "TrafficCodeRepository",
]
