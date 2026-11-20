"""
=============================================================================
CAPA DE LÓGICA — Servicio: ComparadorService
=============================================================================
Gestiona la lógica de comparación de productos aplicando la regla de negocio
de un máximo de 3 artículos en simultáneo y orquestando el modelo
polimórfico ComparadorProductos con el ProductoRepository.
=============================================================================
"""

from typing import List, Dict, Any, Optional
from logica.comparador_productos import ComparadorProductos


class ComparadorService:
    """
    Servicio de la lógica de negocio para la comparación de productos.

    Atributos privados:
        _objRepo: Repositorio de acceso a datos.
    """

    DEFAULTS: Dict[str, List[str]] = {
        "motos": ["ktm-450-exc-f", "husqvarna-te-300", "yamaha-wr450f"],
        "cascos": ["agv-pista-gp-rr", "shoei-x-spr-pro", "arai-rx-7v-evo"],
        "ropa": ["alpinestars-mono-gp-plus-v4", "dainese-laguna-seca-5", "rst-tractech-evo-4"],
    }

    def __init__(self, objRepo: Optional[Any] = None) -> None:
        """
        Constructor del servicio de comparación.
        """
        if objRepo is None:
            from datos.producto_repository import ProductoRepository
            objRepo = ProductoRepository()
        self._objRepo = objRepo

    def comparar(
        self,
        lstProductIds: List[str],
        strCategoria: str = "motos",
        blnAllowDefault: bool = False,
    ) -> Dict[str, Any]:
        """
        Ejecuta la comparación entre los productos especificados.

        Parámetros:
            lstProductIds (list): Lista de identificadores de productos.
            strCategoria (str): Categoría común a comparar.
            blnAllowDefault (bool): Si es True y la lista está vacía, carga defaults.

        Retorna:
            Dict[str, Any]: Estructura con productos, atributos consolidados y estado.

        Lanza:
            ValueError: Si la cantidad de productos supera el límite de 3.
        """
        if len(lstProductIds) > ComparadorProductos.LIMITE_MAXIMO:
            raise ValueError(
                f"El comparador permite un máximo de {ComparadorProductos.LIMITE_MAXIMO} productos simultáneamente."
            )

        todosProductos = self._objRepo.obtenerTodosComoDict()
        seleccionados = [
            p for p in todosProductos
            if p.get("id") in lstProductIds and p.get("category") == strCategoria
        ]

        if len(seleccionados) == 0 and blnAllowDefault:
            defaultIds = self.DEFAULTS.get(strCategoria, self.DEFAULTS["motos"])
            seleccionados = [p for p in todosProductos if p.get("id") in defaultIds]

        # Utilizar el modelo polimórfico ComparadorProductos
        objComparador = ComparadorProductos()
        todosObjetos = self._objRepo.obtenerTodos()
        idsSeleccionados = [s["id"] for s in seleccionados]

        for objP in todosObjetos:
            if objP.intIdProducto in idsSeleccionados:
                objComparador.seleccionarProductos(objP)

        atributos = objComparador.compararEspecificaciones()

        return {
            "category": strCategoria,
            "products": seleccionados,
            "attributes": atributos,
            "max_allowed": ComparadorProductos.LIMITE_MAXIMO,
            "is_empty": len(seleccionados) == 0,
        }
