# Servicio que conecta el asistente virtual con las leyes de transito guardadas.
# Recibe las preguntas del chat y entrega la explicacion legal y fuentes oficiales.

from typing import Dict, Any, Optional
from logica.chatbot import Chatbot


class ChatbotService:
    # Servicio que atiende las preguntas de normas viales que hacen los usuarios.

    def __init__(self, objRepo: Optional[Any] = None) -> None:
        # Carga las leyes desde el repositorio de transito en la memoria del asistente.
        if objRepo is None:
            from datos.traffic_code_repository import TrafficCodeRepository
            objRepo = TrafficCodeRepository()
        self._objRepo = objRepo
        self._objChatbot: Chatbot = Chatbot()

        datosLegales = self._objRepo.obtenerDatosCompletos()
        self._objChatbot.cargarBaseConocimiento(datosLegales)

    # Revisa que la pregunta no este vacia y busca la respuesta legal adecuada.
    def procesarConsulta(self, strMensaje: str) -> Dict[str, Any]:
        if not strMensaje or not strMensaje.strip():
            raise ValueError("Por favor escribe tu consulta sobre las normas de transito.")

        return self._objChatbot.orientarSobreCodigoTransito(strMensaje)

    procesar_consulta = procesarConsulta
