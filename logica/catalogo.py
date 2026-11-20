"""
=============================================================================
CAPA DE LÓGICA — Clase: Catálogo
=============================================================================
Pilar POO: ENCAPSULAMIENTO.

Administra la colección centralizada de productos del sistema GarajeCOL.
Controla las búsquedas, filtros por categoría, marca o precio y la
actualización segura de los productos registrados.
=============================================================================
"""

from typing import List, Optional
from logica.producto import Producto


class Catalogo:
    """
    Clase Catálogo según el diagrama de diseño GarajeCOL.

    ENCAPSULAMIENTO: Atributos privados con nomenclatura estándar (camelCase).
    La lista interna de productos está protegida y sólo se altera mediante
    métodos autorizados como agregarProducto() o actualizarCatalogo().

    Atributos privados:
        _lstProductos (list): Lista interna de objetos Producto.
        _intTotalItemsRegistrados (int): Contador total de productos registrados.
    """

    def __init__(self, lstProductos: Optional[List[Producto]] = None) -> None:
        """
        Constructor del catálogo.
        """
        self._lstProductos: List[Producto] = list(lstProductos) if lstProductos else []
        self._intTotalItemsRegistrados: int = len(self._lstProductos)

    # =========================================================================
    # PROPIEDADES EN CAMELCASE (ENCAPSULAMIENTO)
    # =========================================================================

    @property
    def lstProductos(self) -> List[Producto]:
        """Copia de la lista de productos registrados para evitar mutaciones externas."""
        return list(self._lstProductos)

    @property
    def intTotalItemsRegistrados(self) -> int:
        """Número total de ítems registrados en el catálogo."""
        return self._intTotalItemsRegistrados

    # Aliases de compatibilidad
    productos = lstProductos
    total_items_registrados = intTotalItemsRegistrados

    # =========================================================================
    # MÉTODOS EN CAMELCASE (REQUISITOS DEL DOCUMENTO DE DISEÑO)
    # =========================================================================

    def buscarProductos(self, strCriterio: str) -> List[Producto]:
        """
        Busca productos coincidentes por nombre, marca o badge.

        Parámetros:
            strCriterio (str): Término de búsqueda textual.

        Retorna:
            List[Producto]: Lista de productos que coinciden con el criterio.
        """
        criterioLimpio = strCriterio.lower().strip()
        if not criterioLimpio:
            return list(self._lstProductos)

        coincidencias: List[Producto] = []
        for objProducto in self._lstProductos:
            nombre = objProducto.strNombreProducto.lower()
            marca = objProducto.strMarcaProducto.lower()
            badge = objProducto.strBadge.lower()
            if criterioLimpio in nombre or criterioLimpio in marca or criterioLimpio in badge:
                coincidencias.append(objProducto)
        return coincidencias

    def filtrarPorCategoria(self, strCategoria: str) -> List[Producto]:
        """
        Filtra los productos pertenecientes a una categoría dada.

        Parámetros:
            strCategoria (str): Nombre de la categoría ('motos', 'cascos', 'ropa', 'repuestos').

        Retorna:
            List[Producto]: Lista de productos filtrados.
        """
        categoriaLimpia = strCategoria.lower().strip()
        return [p for p in self._lstProductos if p.strCategoriaProducto == categoriaLimpia]

    def filtrarPorMarca(self, strMarca: str) -> List[Producto]:
        """
        Filtra productos según el fabricante o marca.

        Parámetros:
            strMarca (str): Marca a buscar.

        Retorna:
            List[Producto]: Productos de la marca indicada.
        """
        marcaLimpia = strMarca.lower().strip()
        return [p for p in self._lstProductos if p.strMarcaProducto.lower() == marcaLimpia]

    def filtrarPorPrecioMaximo(self, dblPrecioMax: float) -> List[Producto]:
        """
        Filtra productos cuyo precio no supere el umbral máximo.

        Parámetros:
            dblPrecioMax (float): Límite superior de precio en COP.

        Retorna:
            List[Producto]: Productos dentro del rango presupuestal.
        """
        return [p for p in self._lstProductos if p.dblPrecioProducto <= dblPrecioMax]

    def agregarProducto(self, objProducto: Producto) -> bool:
        """
        Agrega un nuevo producto validando que no esté duplicado por id.

        Parámetros:
            objProducto (Producto): Instancia a incorporar.

        Retorna:
            bool: True si se agregó, False si ya existía.
        """
        idsExistentes = [p.intIdProducto for p in self._lstProductos]
        if objProducto.intIdProducto in idsExistentes:
            return False
        self._lstProductos.append(objProducto)
        self._intTotalItemsRegistrados = len(self._lstProductos)
        return True

    def actualizarCatalogo(self, lstNuevosProductos: Optional[List[Producto]] = None) -> bool:
        """
        Actualiza el catálogo con una nueva colección de productos.

        Parámetros:
            lstNuevosProductos (list, opcional): Colección de reemplazo.

        Retorna:
            bool: True al completar la actualización.
        """
        if lstNuevosProductos is not None:
            self._lstProductos = list(lstNuevosProductos)
            self._intTotalItemsRegistrados = len(self._lstProductos)
        return True

    def obtenerProductoPorId(self, strId: str) -> Optional[Producto]:
        """
        Recupera un producto por su id único.

        Parámetros:
            strId (str): Identificador único.

        Retorna:
            Optional[Producto]: Producto encontrado o None.
        """
        for p in self._lstProductos:
            if p.intIdProducto == strId:
                return p
        return None

    def obtenerDestacados(self) -> List[Producto]:
        """
        Retorna la lista de productos marcados como destacados.

        Retorna:
            List[Producto]: Productos destacados.
        """
        return [p for p in self._lstProductos if p.blnDestacado]

    # Aliases snake_case para compatibilidad
    buscar_productos = buscarProductos
    filtrar_por_categoria = filtrarPorCategoria
    filtrar_por_marca = filtrarPorMarca
    filtrar_por_precio_maximo = filtrarPorPrecioMaximo
    agregar_producto = agregarProducto
    actualizar_catalogo = actualizarCatalogo
    obtener_producto_por_id = obtenerProductoPorId
    obtener_destacados = obtenerDestacados

    def __len__(self) -> int:
        return self._intTotalItemsRegistrados

    def __str__(self) -> str:
        return f"Catálogo GarajeCOL ({self._intTotalItemsRegistrados} productos registrados)"
