"""
=============================================================================
CAPA DE LÓGICA — GarajeCOL
=============================================================================
Módulo principal de la capa de lógica de negocio y dominio del sistema.
Contiene todos los modelos basados en los 4 pilares de la POO:
  - Abstracción: Producto (clase abstracta base).
  - Herencia: Motocicleta, Equipamiento, Repuesto (heredan de Producto).
  - Polimorfismo: obtenerDetalles() y revisarEspecificaciones() especializados.
  - Encapsulamiento: atributos privados con validación y getters en camelCase.

Incluye los servicios de orquestación:
  - CatalogoService, RecomendacionService, ComparadorService, ChatbotService, AuthService.
=============================================================================
"""

from logica.producto import Producto
from logica.motocicleta import Motocicleta
from logica.equipamiento import Equipamiento
from logica.repuesto import Repuesto
from logica.usuario import Usuario
from logica.catalogo import Catalogo
from logica.comparador_productos import ComparadorProductos
from logica.personalizacion import Personalizacion
from logica.chatbot import Chatbot
from logica.plataforma_web import PlataformaWeb

from logica.catalogo_service import CatalogoService
from logica.recomendacion_service import RecomendacionService
from logica.comparador_service import ComparadorService
from logica.chatbot_service import ChatbotService
from logica.auth_service import AuthService

__all__ = [
    # Modelos de Dominio POO
    "Producto",
    "Motocicleta",
    "Equipamiento",
    "Repuesto",
    "Usuario",
    "Catalogo",
    "ComparadorProductos",
    "Personalizacion",
    "Chatbot",
    "PlataformaWeb",
    # Servicios de Lógica de Negocio
    "CatalogoService",
    "RecomendacionService",
    "ComparadorService",
    "ChatbotService",
    "AuthService",
]
