"""
=============================================================================
CAPA DE LÓGICA — Servicio: CatalogoService
=============================================================================
Coordina la interacción entre la capa de datos (ProductoRepository)
y los modelos de dominio (Catalogo, Producto).
Implementa métodos en camelCase con documentación exhaustiva.
=============================================================================
"""

from typing import List, Dict, Any, Optional
from logica.catalogo import Catalogo
from logica.producto import Producto


class CatalogoService:
    """
    Servicio de la lógica de negocio para la gestión del catálogo.

    Atributos privados:
        _objRepo: Repositorio de acceso a datos de productos.
    """

    def __init__(self, objRepo: Optional[Any] = None) -> None:
        """
        Constructor del servicio de catálogo.

        Parámetros:
            objRepo (opcional): Repositorio inyectado.
        """
        if objRepo is None:
            from datos.producto_repository import ProductoRepository
            objRepo = ProductoRepository()
        self._objRepo = objRepo

    def obtenerCatalogoCompleto(self) -> Catalogo:
        """
        Construye la entidad Catalogo a partir de todos los productos del repositorio.

        Retorna:
            Catalogo: Instancia cargada con los objetos Producto.
        """
        listaProductos = self._objRepo.obtenerTodos()
        return Catalogo(lstProductos=listaProductos)

    # Alias snake_case
    obtener_catalogo_completo = obtenerCatalogoCompleto

    def obtenerProductosDestacados(self) -> List[Dict[str, Any]]:
        """
        Recupera los productos destacados en formato de diccionario para la presentación.

        Retorna:
            List[Dict[str, Any]]: Lista de diccionarios de productos destacados.
        """
        catalogo = self.obtenerCatalogoCompleto()
        return [p.toDict() for p in catalogo.obtenerDestacados()]

    # Alias snake_case
    obtener_productos_destacados = obtenerProductosDestacados

    def obtenerProductosPorCategoria(self, strCategoria: str) -> List[Dict[str, Any]]:
        """
        Filtra y serializa los productos de una categoría específica.

        Parámetros:
            strCategoria (str): Categoría a filtrar ('motos', 'cascos', 'ropa', 'repuestos').

        Retorna:
            List[Dict[str, Any]]: Productos filtrados como diccionarios.
        """
        productos = self._objRepo.obtenerPorCategoria(strCategoria)
        return [p.toDict() for p in productos]

    # Alias snake_case
    obtener_productos_por_categoria = obtenerProductosPorCategoria

    def buscarProductos(
        self,
        strCategoria: Optional[str] = None,
        strMarca: Optional[str] = None,
        strConsulta: str = "",
        intPrecioMaximo: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
        """
        Aplica filtros combinados sobre el catálogo de productos.

        Parámetros:
            strCategoria (str, opcional): Categoría requerida.
            strMarca (str, opcional): Marca requerida.
            strConsulta (str): Búsqueda por texto libre.
            intPrecioMaximo (int, opcional): Límite superior de precio.

        Retorna:
            List[Dict[str, Any]]: Colección de productos que satisfacen todos los filtros.
        """
        catalogo = self.obtenerCatalogoCompleto()
        productos: List[Producto] = catalogo.lstProductos

        if strCategoria:
            productos = [p for p in productos if p.strCategoriaProducto == strCategoria.lower().strip()]
        if strMarca:
            productos = [p for p in productos if p.strMarcaProducto.lower() == strMarca.lower().strip()]
        if intPrecioMaximo:
            productos = [p for p in productos if p.dblPrecioProducto <= intPrecioMaximo]
        if strConsulta:
            q = strConsulta.lower().strip()
            productos = [
                p for p in productos
                if q in p.strNombreProducto.lower()
                or q in p.strMarcaProducto.lower()
                or q in p.strBadge.lower()
            ]

        return [p.toDict() for p in productos]

    # Alias snake_case
    buscar_productos = buscarProductos

    def obtenerDetalleProducto(self, strProductoId: str) -> Optional[Dict[str, Any]]:
        """
        Busca un producto por su id y retorna su diccionario de presentación.

        Parámetros:
            strProductoId (str): Identificador del producto.

        Retorna:
            Optional[Dict[str, Any]]: Diccionario del producto o None.
        """
        objProducto = self._objRepo.obtenerPorId(strProductoId)
        if objProducto:
            return objProducto.toDict()
        return None

    # Alias snake_case
    obtener_detalle_producto = obtenerDetalleProducto

    def obtenerTodosComoDict(self) -> List[Dict[str, Any]]:
        """
        Retorna la lista de diccionarios de productos directamente del repositorio.

        Retorna:
            List[Dict[str, Any]]: Colección de diccionarios de productos.
        """
        return self._objRepo.obtenerTodosComoDict()

    # Alias snake_case
    obtener_todos_como_dict = obtenerTodosComoDict
