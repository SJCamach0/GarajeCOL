"""
=============================================================================
CAPA DE DATOS — ProductoRepository
=============================================================================
Clase encargada de la persistencia y recuperación de productos desde
el archivo JSON oficial. Utiliza el patrón Factory para instanciar
los objetos especializados de la capa de lógica (Motocicleta, Equipamiento,
Repuesto), garantizando la separación estricta de responsabilidades.
=============================================================================
"""

import os
import json
from typing import List, Optional, Dict, Any

from logica.motocicleta import Motocicleta
from logica.equipamiento import Equipamiento
from logica.repuesto import Repuesto
from logica.producto import Producto


class ProductoRepository:
    """
    Repositorio de datos para el Catálogo de Productos.

    Atributos privados:
        _strRutaDatos (str): Ruta al directorio donde residen los datos.
        _strRutaArchivo (str): Ruta completa al archivo products.json.
    """

    def __init__(self, strRutaDatos: Optional[str] = None) -> None:
        """
        Constructor del repositorio de productos.

        Parámetros:
            strRutaDatos (str, opcional): Ruta al directorio de datos.
                                          Si no se proporciona, busca 'datos/'
                                          o 'data/' en el proyecto.
        """
        directorioBase = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if strRutaDatos is None:
            # Buscar primero en datos/, luego en data/
            posibleRuta = os.path.join(directorioBase, "datos")
            if os.path.exists(os.path.join(posibleRuta, "products.json")):
                strRutaDatos = posibleRuta
            else:
                strRutaDatos = os.path.join(directorioBase, "data")

        self._strRutaDatos = strRutaDatos
        self._strRutaArchivo = os.path.join(strRutaDatos, "products.json")

    def obtenerTodos(self) -> List[Producto]:
        """
        Lee el archivo de datos y transforma cada elemento JSON en un
        objeto de la jerarquía de Producto (Motocicleta, Equipamiento, Repuesto).

        Retorna:
            List[Producto]: Lista de instancias polimórficas de Producto.
        """
        listaJson = self._leerJson()
        listaProductos: List[Producto] = []

        for item in listaJson:
            objProducto = self._crearProductoDesdeDiccionario(item)
            if objProducto is not None:
                listaProductos.append(objProducto)

        return listaProductos

    # Alias snake_case para compatibilidad
    obtener_todos = obtenerTodos

    def obtenerTodosComoDict(self) -> List[Dict[str, Any]]:
        """
        Retorna la lista de productos como diccionarios puros, preservando
        el formato exacto del archivo JSON.

        Retorna:
            List[Dict[str, Any]]: Colección de diccionarios de productos.
        """
        return self._leerJson()

    # Alias snake_case para compatibilidad
    obtener_todos_como_dict = obtenerTodosComoDict

    def obtenerPorId(self, strId: str) -> Optional[Producto]:
        """
        Busca un producto por su identificador único dentro del catálogo.

        Parámetros:
            strId (str): Identificador único del producto (slug).

        Retorna:
            Optional[Producto]: Instancia del producto si existe, o None.
        """
        lista = self.obtenerTodos()
        for objProducto in lista:
            if objProducto.intIdProducto == strId:
                return objProducto
        return None

    # Alias snake_case para compatibilidad
    obtener_por_id = obtenerPorId

    def obtenerPorCategoria(self, strCategoria: str) -> List[Producto]:
        """
        Filtra los productos pertenecientes a una categoría específica.

        Parámetros:
            strCategoria (str): Categoría a filtrar ('motos', 'cascos', 'ropa', 'repuestos').

        Retorna:
            List[Producto]: Lista de productos que coinciden con la categoría.
        """
        categoriaLimpia = strCategoria.lower().strip()
        return [p for p in self.obtenerTodos() if p.strCategoriaProducto == categoriaLimpia]

    # Alias snake_case para compatibilidad
    obtener_por_categoria = obtenerPorCategoria

    # =========================================================================
    # MÉTODOS PRIVADOS / AUXILIARES
    # =========================================================================

    def _leerJson(self) -> List[Dict[str, Any]]:
        """
        Lee y decodifica el archivo JSON en codificación UTF-8.

        Retorna:
            List[Dict[str, Any]]: Datos decodificados del JSON.
        """
        with open(self._strRutaArchivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def _crearProductoDesdeDiccionario(self, dictItem: Dict[str, Any]) -> Optional[Producto]:
        """
        Patrón Factory Method: instancia la subclase de Producto adecuada
        (Motocicleta, Equipamiento o Repuesto) según el campo 'category'.

        Parámetros:
            dictItem (Dict[str, Any]): Diccionario con los datos del producto.

        Retorna:
            Optional[Producto]: Instancia especializada de Producto.
        """
        strCategoria = dictItem.get("category", "")

        argumentosComunes = {
            "intIdProducto": str(dictItem.get("id", "")),
            "strNombreProducto": dictItem.get("name", ""),
            "strCategoriaProducto": strCategoria,
            "strMarcaProducto": dictItem.get("brand", ""),
            "dblPrecioProducto": float(dictItem.get("price", 0.0)),
            "strEnlaceTiendaOficial": dictItem.get("official_url", ""),
            "strImagen": dictItem.get("image", ""),
            "strImagenGrande": dictItem.get("image_large", ""),
            "lstMiniaturas": dictItem.get("thumbnails", []),
            "strNombreTiendaOficial": dictItem.get("official_store_name", ""),
            "strDescripcion": dictItem.get("description", ""),
            "dictEspecificaciones": dictItem.get("specs", {}),
            "strNombreCategoria": dictItem.get("category_name", strCategoria.capitalize()),
            "strBadge": dictItem.get("badge", ""),
            "blnDestacado": dictItem.get("featured", False),
            "blnMejorValor": dictItem.get("best_value", False),
            "strPrecioFormateado": dictItem.get("price_formatted", ""),
            "strTierPrecio": dictItem.get("price_tier", ""),
        }

        if strCategoria == "motos":
            return Motocicleta(
                dblCilindrajeMotocicleta=float(dictItem.get("displacement", 0)),
                strTipoFrenosMotocicleta=dictItem.get("specs", {}).get("Sistema de frenos", ""),
                dblCapacidadTanque=0.0,
                dblTorqueMotocicleta=0.0,
                dblPesoMotocicleta=0.0,
                intModeloMotocicleta=2026,
                strTipo=dictItem.get("type", ""),
                strTipoNombre=dictItem.get("type_name", ""),
                intCilindraje=int(dictItem.get("displacement", 0)),
                strTierCilindraje=dictItem.get("displacement_tier", ""),
                **argumentosComunes,
            )
        elif strCategoria in ("cascos", "ropa"):
            return Equipamiento(
                strTallaEquipamiento=dictItem.get("specs", {}).get("Tallas disponibles", ""),
                strMaterialFabricacion=dictItem.get("specs", {}).get("Material de calota", ""),
                strSubcategoria=strCategoria,
                **argumentosComunes,
            )
        else:
            return Repuesto(**argumentosComunes)
