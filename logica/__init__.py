# Capa de logica: agrupa las clases de los productos, usuarios y servicios.
# Contiene las reglas del negocio como filtros, comparaciones y recomendaciones.

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

# Lista de clases y servicios disponibles para importar en la aplicacion.
__all__ = [
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
    "CatalogoService",
    "RecomendacionService",
    "ComparadorService",
    "ChatbotService",
    "AuthService",
]
