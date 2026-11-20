# Se encarga de cargar los productos desde el archivo JSON oficial.
# Convierte los datos en objetos de moto, equipamiento o repuesto.

import os
import json
from typing import List, Optional, Dict, Any

from logica.motocicleta import Motocicleta
from logica.equipamiento import Equipamiento
from logica.repuesto import Repuesto
from logica.producto import Producto


class ProductoRepository:
    # Lee y administra la lista de productos guardada en el archivo JSON.

    def __init__(self, strRutaDatos: Optional[str] = None) -> None:
        # Busca la carpeta de datos y define la ruta del archivo products.json.
        directorioBase = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        if strRutaDatos is None:
            strRutaDatos = os.path.join(directorioBase, "datos")

        self._strRutaDatos = strRutaDatos
        self._strRutaArchivo = os.path.join(strRutaDatos, "products.json")

    def obtenerTodos(self) -> List[Producto]:
        # Lee el JSON y devuelve la lista completa de productos convertidos en objetos.
        listaJson = self._leerJson()
        listaProductos: List[Producto] = []

        for item in listaJson:
            objProducto = self._crearProductoDesdeDiccionario(item)
            if objProducto is not None:
                listaProductos.append(objProducto)

        return listaProductos

    obtener_todos = obtenerTodos

    def obtenerTodosComoDict(self) -> List[Dict[str, Any]]:
        # Devuelve todos los productos en formato de diccionario simple.
        return self._leerJson()

    obtener_todos_como_dict = obtenerTodosComoDict

    def obtenerPorId(self, strId: str) -> Optional[Producto]:
        # Busca un producto en la lista utilizando su identificador unico.
        lista = self.obtenerTodos()
        for objProducto in lista:
            if objProducto.intIdProducto == strId:
                return objProducto
        return None

    obtener_por_id = obtenerPorId

    def obtenerPorCategoria(self, strCategoria: str) -> List[Producto]:
        # Filtra y devuelve solo los productos que pertenecen a una categoria dada.
        categoriaLimpia = strCategoria.lower().strip()
        return [p for p in self.obtenerTodos() if p.strCategoriaProducto == categoriaLimpia]

    obtener_por_categoria = obtenerPorCategoria

    def _leerJson(self) -> List[Dict[str, Any]]:
        # Abre y lee el archivo JSON de productos con texto en espanol.
        with open(self._strRutaArchivo, "r", encoding="utf-8") as archivo:
            return json.load(archivo)

    def _crearProductoDesdeDiccionario(self, dictItem: Dict[str, Any]) -> Optional[Producto]:
        # Crea el tipo de objeto correcto (Moto, Equipamiento o Repuesto) segun los datos.
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
