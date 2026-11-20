# Servicio que conecta la pantalla con los productos guardados en los archivos.
# Aplica los filtros de busqueda en tiempo real por precio, categoria, marca o nombre.

from typing import List, Dict, Any, Optional
from logica.catalogo import Catalogo
from logica.producto import Producto


class CatalogoService:
    # Servicio que atiende las solicitudes de productos desde las paginas web.

    def __init__(self, objRepo: Optional[Any] = None) -> None:
        # Conecta el servicio con el repositorio que lee el archivo JSON de productos.
        if objRepo is None:
            from datos.producto_repository import ProductoRepository
            objRepo = ProductoRepository()
        self._objRepo = objRepo

    # Carga todos los productos desde el archivo y crea el Catalogo general.
    def obtenerCatalogoCompleto(self) -> Catalogo:
        listaProductos = self._objRepo.obtenerTodos()
        return Catalogo(lstProductos=listaProductos)

    obtener_catalogo_completo = obtenerCatalogoCompleto

    # Devuelve la lista de productos destacados para mostrar en la pagina principal.
    def obtenerProductosDestacados(self) -> List[Dict[str, Any]]:
        catalogo = self.obtenerCatalogoCompleto()
        return [p.toDict() for p in catalogo.obtenerDestacados()]

    obtener_productos_destacados = obtenerProductosDestacados

    # Devuelve los productos filtrados por categoria: motos, cascos, ropa o repuestos.
    def obtenerProductosPorCategoria(self, strCategoria: str) -> List[Dict[str, Any]]:
        productos = self._objRepo.obtenerPorCategoria(strCategoria)
        return [p.toDict() for p in productos]

    obtener_productos_por_categoria = obtenerProductosPorCategoria

    # Aplica multiples filtros al mismo tiempo: categoria, marca, precio maximo o texto.
    def buscarProductos(
        self,
        strCategoria: Optional[str] = None,
        strMarca: Optional[str] = None,
        strConsulta: str = "",
        intPrecioMaximo: Optional[int] = None,
    ) -> List[Dict[str, Any]]:
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

    buscar_productos = buscarProductos

    # Busca un producto por su id para mostrar su ficha tecnica detallada.
    def obtenerDetalleProducto(self, strProductoId: str) -> Optional[Dict[str, Any]]:
        objProducto = self._objRepo.obtenerPorId(strProductoId)
        if objProducto:
            return objProducto.toDict()
        return None

    obtener_detalle_producto = obtenerDetalleProducto

    # Devuelve todos los productos en formato de lista para respuestas directas.
    def obtenerTodosComoDict(self) -> List[Dict[str, Any]]:
        return self._objRepo.obtenerTodosComoDict()

    obtener_todos_como_dict = obtenerTodosComoDict
