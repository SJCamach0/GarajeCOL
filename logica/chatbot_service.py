"""
=============================================================================
CAPA DE LÓGICA — Servicio: ChatbotService
=============================================================================
Conecta el modelo Chatbot con el repositorio TrafficCodeRepository,
cargando la base de conocimiento legal colombiana y procesando
las consultas viales de los usuarios.
=============================================================================
"""

from typing import Dict, Any, Optional
from logica.chatbot import Chatbot


class ChatbotService:
    """
    Servicio de la lógica de negocio para la asistencia normativa vial.

    Atributos privados:
        _objRepo: Repositorio de la normativa legal.
        _objChatbot (Chatbot): Modelo de dominio que procesa las consultas.
    """

    def __init__(self, objRepo: Optional[Any] = None) -> None:
        """
        Constructor del servicio de chatbot.
        """
        if objRepo is None:
            from datos.traffic_code_repository import TrafficCodeRepository
            objRepo = TrafficCodeRepository()
        self._objRepo = objRepo
        self._objChatbot: Chatbot = Chatbot()

        # Inyectar la base de conocimiento legal en el modelo Chatbot
        datosLegales = self._objRepo.obtenerDatosCompletos()
        self._objChatbot.cargarBaseConocimiento(datosLegales)

    def procesarConsulta(self, strMensaje: str) -> Dict[str, Any]:
        """
        Valida y procesa la consulta del usuario delegándola al modelo Chatbot.

        Parámetros:
            strMensaje (str): Texto de la consulta vial.

        Retorna:
            Dict[str, Any]: Respuesta estructurada con fundamentación y fuentes.

        Lanza:
            ValueError: Si el mensaje está vacío.
        """
        if not strMensaje or not strMensaje.strip():
            raise ValueError("Por favor escribe tu consulta sobre las normas de tránsito.")

        return self._objChatbot.orientarSobreCodigoTransito(strMensaje)

    # Alias snake_case
    procesar_consulta = procesarConsulta
