# Lee el archivo JSON que contiene las leyes y normas de transito en Colombia.
# Suministra los articulos legales que usa el asistente de preguntas frecuentes.

import os
import json
from typing import Dict, Any, List, Optional


class TrafficCodeRepository:
    # Repositorio para consultar los articulos y normas viales guardadas en JSON.

    def __init__(self, strRutaDatos: Optional[str] = None) -> None:
        # Define la ruta hacia el archivo traffic_code.json dentro de la carpeta datos.
        directorioBase = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if strRutaDatos is None:
            strRutaDatos = os.path.join(directorioBase, "datos")

        self._strRutaDatos = strRutaDatos
        self._strRutaArchivo = os.path.join(strRutaDatos, "traffic_code.json")

    def obtenerDatosCompletos(self) -> Dict[str, Any]:
        # Devuelve toda la informacion del archivo: articulos, fuentes y avisos legales.
        return self._leerJson()

    obtener_datos_completos = obtenerDatosCompletos

    def obtenerTopics(self) -> List[Dict[str, Any]]:
        # Devuelve la lista de temas sobre casco, velocidad, soat y tecnomecanica.
        datos = self._leerJson()
        return datos.get("topics", [])

    obtener_topics = obtenerTopics

    def obtenerDisclaimer(self) -> str:
        # Devuelve el mensaje legal que aclara que la informacion es solo educativa.
        datos = self._leerJson()
        return datos.get("disclaimer", "")

    obtener_disclaimer = obtenerDisclaimer

    def obtenerFuentesOficiales(self) -> List[Dict[str, Any]]:
        # Devuelve los enlaces a entidades oficiales como MinTransporte y RUNT.
        datos = self._leerJson()
        return datos.get("official_sources", [])

    obtener_fuentes_oficiales = obtenerFuentesOficiales

    def _leerJson(self) -> Dict[str, Any]:
        # Abre y lee el archivo traffic_code.json con formato de texto en espanol.
        with open(self._strRutaArchivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
