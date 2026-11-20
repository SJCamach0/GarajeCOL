"""
=============================================================================
CAPA DE LÓGICA — Clase: Chatbot
=============================================================================
Pilar POO: ENCAPSULAMIENTO.

Asistente virtual de orientación normativa vial para motociclistas en Colombia.
Maneja el historial de consultas, la sesión del usuario y la base de
conocimiento de la Ley 769 de 2002 (Código Nacional de Tránsito), Ley 2251
de 2022 (Ley Julián Esteban) y resoluciones del Ministerio de Transporte.
=============================================================================
"""

from typing import List, Dict, Any, Optional


class Chatbot:
    """
    Clase Chatbot según el modelado de diseño GarajeCOL.

    ENCAPSULAMIENTO: Atributos privados con nomenclatura estándar (camelCase).
    La base de conocimiento legal se administra internamente sin permitir
    modificaciones directas no autorizadas.

    Atributos privados:
        _lstHistorialConsultas (list): Registro histórico de preguntas realizadas.
        _intIdentificadorSesion (int): Identificador numérico de la sesión.
        _objBaseConocimientoLegal (dict): Contenido de la normativa colombiana.
    """

    def __init__(
        self,
        lstHistorialConsultas: Optional[List[Dict[str, Any]]] = None,
        intIdentificadorSesion: int = 1,
        objBaseConocimientoLegal: Optional[Dict[str, Any]] = None,
    ) -> None:
        """
        Constructor de la clase Chatbot.
        """
        self._lstHistorialConsultas: List[Dict[str, Any]] = lstHistorialConsultas or []
        self._intIdentificadorSesion: int = intIdentificadorSesion
        self._objBaseConocimientoLegal: Dict[str, Any] = objBaseConocimientoLegal or {}

    # =========================================================================
    # PROPIEDADES EN CAMELCASE (ENCAPSULAMIENTO)
    # =========================================================================

    @property
    def lstHistorialConsultas(self) -> List[Dict[str, Any]]:
        """Historial de consultas de la sesión."""
        return list(self._lstHistorialConsultas)

    @property
    def intIdentificadorSesion(self) -> int:
        """ID de sesión del chatbot."""
        return self._intIdentificadorSesion

    @property
    def objBaseConocimientoLegal(self) -> Dict[str, Any]:
        """Base de conocimiento cargada."""
        return dict(self._objBaseConocimientoLegal)

    # Aliases de compatibilidad
    historial_consultas = lstHistorialConsultas
    identificador_sesion = intIdentificadorSesion

    # =========================================================================
    # MÉTODOS EN CAMELCASE (REQUISITOS DEL DOCUMENTO DE DISEÑO)
    # =========================================================================

    def cargarBaseConocimiento(self, dictDatos: Dict[str, Any]) -> None:
        """
        Carga la base de datos legal en la memoria interna del chatbot.

        Parámetros:
            dictDatos (dict): Diccionario con topics, fuentes y disclaimer.
        """
        self._objBaseConocimientoLegal = dictDatos

    def orientarSobreCodigoTransito(self, strConsulta: str) -> Dict[str, Any]:
        """
        Analiza la consulta del usuario, identifica el artículo o tema
        más relevante del Código Nacional de Tránsito y estructura la respuesta.

        Parámetros:
            strConsulta (str): Pregunta o inquietud del motociclista.

        Retorna:
            Dict[str, Any]: Respuesta formateada, fuente oficial, disclaimer y fuentes.
        """
        consultaLimpia = strConsulta.lower().strip()
        temas = self._objBaseConocimientoLegal.get("topics", [])
        disclaimer = self._objBaseConocimientoLegal.get("disclaimer", "")
        fuentesOficiales = self._objBaseConocimientoLegal.get("official_sources", [])

        mejorTema = None
        mejorPuntaje = 0

        for tema in temas:
            puntaje = 0
            for palabraClave in tema.get("keywords", []):
                if palabraClave in consultaLimpia:
                    puntaje += 2
            for palabra in tema.get("title", "").lower().split():
                if len(palabra) > 3 and palabra in consultaLimpia:
                    puntaje += 1
            if puntaje > mejorPuntaje:
                mejorPuntaje = puntaje
                mejorTema = tema

        if mejorTema and mejorPuntaje >= 1:
            textoReglas = "\n".join([f"• {r}" for r in mejorTema.get("key_rules", [])])
            respuesta = (
                f"**{mejorTema['title']}**\n\n"
                f"📋 **Fundamento Legal Oficial:** {mejorTema['norm']}\n\n"
                f"{mejorTema['summary']}\n\n"
                f"**Reglas y consideraciones clave:**\n{textoReglas}\n\n"
                f"⚠️ **Sanción aplicable:** {mejorTema['sanction']}\n\n"
                f"🔗 **Fuente Oficial:** [{mejorTema['norm']}]({mejorTema['source_url']})"
            )
            fuente = {
                "name": "Ministerio de Transporte de Colombia / Código Nacional de Tránsito",
                "norm": mejorTema["norm"],
                "url": mejorTema["source_url"],
            }
        else:
            respuesta = (
                "He analizado tu consulta en la normativa vial colombiana para motociclistas.\n\n"
                "El Código Nacional de Tránsito (Ley 769 de 2002) y la Ley 2251 de 2022 "
                "establecen reglas claras para los motociclistas en Colombia:\n\n"
                "• **Casco reglamentario:** Obligatorio, certificado (ECE/DOT), abrochado "
                "bajo el mentón y visor cerrado (Res. 20203040023385).\n"
                "• **Prendas reflectivas:** Obligatorias de 6:00 p.m. a 6:00 a.m. (Art. 94 Ley 769).\n"
                "• **Velocidad máxima:** 50 km/h en ciudad y 30 km/h en áreas residenciales/escolares "
                "(Ley Julián Esteban).\n"
                "• **Luces encendidas:** 24 horas del día obligatoriamente.\n"
                "• **Documentación:** Licencia A1/A2, Tarjeta de Propiedad, SOAT digital y RTM vigente.\n\n"
                "¿Deseas profundizar en alguna de estas normas o sobre multas específicas?"
            )
            fuente = {
                "name": "Ministerio de Transporte de Colombia",
                "norm": "Ley 769 de 2002 & Ley 2251 de 2022",
                "url": "https://www.mintransporte.gov.co",
            }

        # Registrar en el historial de la sesión
        self._lstHistorialConsultas.append({
            "consulta": strConsulta,
            "temaEncontrado": mejorTema["title"] if mejorTema else "General",
        })

        return {
            "reply": respuesta,
            "official_source": fuente,
            "disclaimer": disclaimer,
            "all_sources": fuentesOficiales,
        }

    def responderConsultasLegales(self, strPregunta: str) -> str:
        """
        Método de alto nivel: responde directamente con el texto explicativo.

        Parámetros:
            strPregunta (str): Pregunta jurídica formulada.

        Retorna:
            str: Respuesta textual orientadora.
        """
        resultado = self.orientarSobreCodigoTransito(strPregunta)
        return resultado["reply"]

    def buscarArticulosCodigo(self, intArticulo: int) -> str:
        """
        Busca un artículo específico por su número en el Código Nacional de Tránsito.

        Parámetros:
            intArticulo (int): Número del artículo a buscar.

        Retorna:
            str: Detalle de la norma aplicable.
        """
        return self.responderConsultasLegales(f"artículo {intArticulo}")

    def interpretarNormasViales(self, strNorma: str) -> str:
        """
        Interpreta una norma o resolución específica del Ministerio de Transporte.

        Parámetros:
            strNorma (str): Nombre o referencia de la norma.

        Retorna:
            str: Interpretación comprensible de la norma.
        """
        return self.responderConsultasLegales(strNorma)

    # Aliases snake_case para compatibilidad
    cargar_base_conocimiento = cargarBaseConocimiento
    orientar_sobre_codigo_transito = orientarSobreCodigoTransito
    responder_consultas_legales = responderConsultasLegales
    buscar_articulos_codigo = buscarArticulosCodigo
    interpretar_normas_viales = interpretarNormasViales

    def __str__(self) -> str:
        return f"Chatbot(Sesión {self._intIdentificadorSesion}, {len(self._lstHistorialConsultas)} consultas)"
