"""
=============================================================================
CAPA DE DATOS — TrafficCodeRepository
=============================================================================
Repositorio encargado de leer y proveer la base de conocimiento legal
sobre el Código Nacional de Tránsito de Colombia (Ley 769 de 2002 y
Ley 2251 de 2022) desde su archivo JSON.
=============================================================================
"""

import os
import json
from typing import Dict, Any, List, Optional


class TrafficCodeRepository:
    """
    Repositorio para el acceso a la normativa de tránsito vial.

    Atributos privados:
        _strRutaDatos (str): Directorio donde se localiza el archivo.
        _strRutaArchivo (str): Ruta completa al archivo traffic_code.json.
    """

    def __init__(self, strRutaDatos: Optional[str] = None) -> None:
        """
        Constructor del repositorio de tránsito.

        Parámetros:
            strRutaDatos (str, opcional): Ruta al directorio de datos.
        """
        directorioBase = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if strRutaDatos is None:
            posibleRuta = os.path.join(directorioBase, "datos")
            if os.path.exists(os.path.join(posibleRuta, "traffic_code.json")):
                strRutaDatos = posibleRuta
            else:
                strRutaDatos = os.path.join(directorioBase, "data")

        self._strRutaDatos = strRutaDatos
        self._strRutaArchivo = os.path.join(strRutaDatos, "traffic_code.json")

    def obtenerDatosCompletos(self) -> Dict[str, Any]:
        """
        Lee y devuelve todo el contenido estructurado de la normativa.

        Retorna:
            Dict[str, Any]: Diccionario con 'topics', 'disclaimer' y 'official_sources'.
        """
        return self._leerJson()

    # Alias snake_case para compatibilidad
    obtener_datos_completos = obtenerDatosCompletos

    def obtenerTopics(self) -> List[Dict[str, Any]]:
        """
        Devuelve únicamente los temas y artículos normativos.

        Retorna:
            List[Dict[str, Any]]: Lista de temas del código de tránsito.
        """
        datos = self._leerJson()
        return datos.get("topics", [])

    # Alias snake_case para compatibilidad
    obtener_topics = obtenerTopics

    def obtenerDisclaimer(self) -> str:
        """
        Devuelve el descargo de responsabilidad legal.

        Retorna:
            str: Texto legal del disclaimer.
        """
        datos = self._leerJson()
        return datos.get("disclaimer", "")

    # Alias snake_case para compatibilidad
    obtener_disclaimer = obtenerDisclaimer

    def obtenerFuentesOficiales(self) -> List[Dict[str, Any]]:
        """
        Devuelve las fuentes oficiales del Ministerio de Transporte.

        Retorna:
            List[Dict[str, Any]]: Lista de enlaces y entidades oficiales.
        """
        datos = self._leerJson()
        return datos.get("official_sources", [])

    # Alias snake_case para compatibilidad
    obtener_fuentes_oficiales = obtenerFuentesOficiales

    # =========================================================================
    # MÉTODOS PRIVADOS
    # =========================================================================

    def _leerJson(self) -> Dict[str, Any]:
        """
        Lee el archivo traffic_code.json en UTF-8.

        Retorna:
            Dict[str, Any]: Contenido parseado del JSON.
        """
        with open(self._strRutaArchivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
