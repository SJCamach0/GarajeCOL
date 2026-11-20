# Asistente virtual que responde dudas sobre las normas de transito de Colombia.
# Busca palabras clave en la pregunta del usuario y devuelve el articulo correspondiente.

from typing import List, Dict, Any, Optional


class Chatbot:
    # Maneja la conversacion y busca las leyes viales para motociclistas.

    def __init__(
        self,
        lstHistorialConsultas: Optional[List[Dict[str, Any]]] = None,
        intIdentificadorSesion: int = 1,
        objBaseConocimientoLegal: Optional[Dict[str, Any]] = None,
    ) -> None:
        # Guarda el historial de preguntas, el id de sesion y las normas de transito.
        self._lstHistorialConsultas: List[Dict[str, Any]] = lstHistorialConsultas or []
        self._intIdentificadorSesion: int = intIdentificadorSesion
        self._objBaseConocimientoLegal: Dict[str, Any] = objBaseConocimientoLegal or {}

    # Propiedades para leer el historial, la sesion y la base de normas.
    @property
    def lstHistorialConsultas(self) -> List[Dict[str, Any]]:
        return list(self._lstHistorialConsultas)

    @property
    def intIdentificadorSesion(self) -> int:
        return self._intIdentificadorSesion

    @property
    def objBaseConocimientoLegal(self) -> Dict[str, Any]:
        return dict(self._objBaseConocimientoLegal)

    historial_consultas = lstHistorialConsultas
    identificador_sesion = intIdentificadorSesion

    # Recibe los datos del archivo JSON para que el asistente tenga las leyes en memoria.
    def cargarBaseConocimiento(self, dictDatos: Dict[str, Any]) -> None:
        self._objBaseConocimientoLegal = dictDatos

    # Busca en las leyes colombianas el tema mas parecido a la pregunta del usuario.
    def orientarSobreCodigoTransito(self, strConsulta: str) -> Dict[str, Any]:
        consultaLimpia = strConsulta.lower().strip()
        temas = self._objBaseConocimientoLegal.get("topics", [])
        faqs = self._objBaseConocimientoLegal.get("faq", [])
        disclaimer = self._objBaseConocimientoLegal.get("disclaimer", "")
        fuentesOficiales = self._objBaseConocimientoLegal.get("official_sources", [])

        # Revisa primero si la pregunta coincide directamente con una duda frecuente (FAQ).
        for item in faqs:
            pregunta = item.get("q", "").lower()
            palabrasClave = [p for p in pregunta.replace("¿", "").replace("?", "").split() if len(p) > 3]
            coincidencias = sum(1 for p in palabrasClave if p in consultaLimpia)
            if len(palabrasClave) > 0 and (coincidencias / len(palabrasClave)) >= 0.5:
                respuesta = (
                    f"**{item['q']}**\n\n"
                    f"{item['a']}\n\n"
                    f"📋 **Fundamento Legal Oficial:** {item.get('norm', 'Ministerio de Transporte')}\n\n"
                    f"🔗 **Fuente Oficial:** [{item.get('norm', 'Consultar norma')}]({item.get('source_url', 'https://www.mintransporte.gov.co')})"
                )
                fuente = {
                    "name": "Ministerio de Transporte de Colombia",
                    "norm": item.get("norm", "Normativa Nacional de Tránsito"),
                    "url": item.get("source_url", "https://www.mintransporte.gov.co"),
                }
                self._lstHistorialConsultas.append({
                    "consulta": strConsulta,
                    "temaEncontrado": item["q"],
                })
                return {
                    "reply": respuesta,
                    "official_source": fuente,
                    "disclaimer": disclaimer,
                    "all_sources": fuentesOficiales,
                }

        # Si no es pregunta rapida, busca el tema por puntaje de palabras clave.
        mejorTema = None
        mejorPuntaje = 0

        for tema in temas:
            puntaje = 0
            for palabraClave in tema.get("keywords", []):
                if palabraClave in consultaLimpia:
                    puntaje += 4 if " " in palabraClave else 2
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

    # Devuelve solo el texto de la respuesta a la pregunta del usuario.
    def responderConsultasLegales(self, strPregunta: str) -> str:
        resultado = self.orientarSobreCodigoTransito(strPregunta)
        return resultado["reply"]

    # Busca la informacion de un articulo especifico del codigo de transito.
    def buscarArticulosCodigo(self, intArticulo: int) -> str:
        return self.responderConsultasLegales(f"articulo {intArticulo}")

    # Explica en palabras sencillas una resolucion del ministerio de transporte.
    def interpretarNormasViales(self, strNorma: str) -> str:
        return self.responderConsultasLegales(strNorma)

    cargar_base_conocimiento = cargarBaseConocimiento
    orientar_sobre_codigo_transito = orientarSobreCodigoTransito
    responder_consultas_legales = responderConsultasLegales
    buscar_articulos_codigo = buscarArticulosCodigo
    interpretar_normas_viales = interpretarNormasViales

    def __str__(self) -> str:
        return f"Chatbot(Sesion {self._intIdentificadorSesion}, {len(self._lstHistorialConsultas)} consultas)"
