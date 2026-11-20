# Administra la lista de todos los productos disponibles en GarajeCOL.
# Permite realizar busquedas, aplicar filtros de categoria, marca o precio y agregar nuevos items.

from typing import List, Optional
from logica.producto import Producto


class Catalogo:
    # Coleccion que agrupa y organiza todos los productos del sistema.

    def __init__(self, lstProductos: Optional[List[Producto]] = None) -> None:
        # Guarda la lista de productos y calcula cuantos productos hay registrados.
        self._lstProductos: List[Producto] = list(lstProductos) if lstProductos else []
        self._intTotalItemsRegistrados: int = len(self._lstProductos)

    # Propiedades para consultar los productos y la cantidad total.
    @property
    def lstProductos(self) -> List[Producto]:
        return list(self._lstProductos)

    @property
    def intTotalItemsRegistrados(self) -> int:
        return self._intTotalItemsRegistrados

    # Nombres faciles para acceder a la lista y al total.
    productos = lstProductos
    total_items_registrados = intTotalItemsRegistrados

    # Busca productos que coincidan con el texto escrito en el buscador.
    def buscarProductos(self, strCriterio: str) -> List[Producto]:
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

    # Devuelve unicamente los productos que pertenecen a la categoria seleccionada.
    def filtrarPorCategoria(self, strCategoria: str) -> List[Producto]:
        categoriaLimpia = strCategoria.lower().strip()
        return [p for p in self._lstProductos if p.strCategoriaProducto == categoriaLimpia]

    # Filtra los productos de una marca especifica como Yamaha, KTM o Brembo.
    def filtrarPorMarca(self, strMarca: str) -> List[Producto]:
        marcaLimpia = strMarca.lower().strip()
        return [p for p in self._lstProductos if p.strMarcaProducto.lower() == marcaLimpia]

    # Filtra los productos cuyo precio este dentro del presupuesto maximo.
    def filtrarPorPrecioMaximo(self, dblPrecioMax: float) -> List[Producto]:
        return [p for p in self._lstProductos if p.dblPrecioProducto <= dblPrecioMax]

    # Agrega un nuevo producto a la lista si no se encuentra registrado previamente.
    def agregarProducto(self, objProducto: Producto) -> bool:
        idsExistentes = [p.intIdProducto for p in self._lstProductos]
        if objProducto.intIdProducto in idsExistentes:
            return False
        self._lstProductos.append(objProducto)
        self._intTotalItemsRegistrados = len(self._lstProductos)
        return True

    # Reemplaza o actualiza la lista de productos del catalogo con una nueva.
    def actualizarCatalogo(self, lstNuevosProductos: Optional[List[Producto]] = None) -> bool:
        if lstNuevosProductos is not None:
            self._lstProductos = list(lstNuevosProductos)
            self._intTotalItemsRegistrados = len(self._lstProductos)
        return True

    # Busca y devuelve un producto usando su codigo o identificador unico.
    def obtenerProductoPorId(self, strId: str) -> Optional[Producto]:
        for p in self._lstProductos:
            if p.intIdProducto == strId:
                return p
        return None

    # Devuelve los productos seleccionados para mostrar en la pagina de inicio.
    def obtenerDestacados(self) -> List[Producto]:
        return [p for p in self._lstProductos if p.blnDestacado]

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
        return f"Catalogo GarajeCOL ({self._intTotalItemsRegistrados} productos registrados)"
