# Servicio que organiza la comparacion de productos en pantalla.
# Aplica la regla de no permitir mas de 3 productos al mismo tiempo.

from typing import List, Dict, Any, Optional
from logica.comparador_productos import ComparadorProductos


class ComparadorService:
    # Servicio que coordina la tabla comparativa de productos para la web.

    DEFAULTS: Dict[str, List[str]] = {
        "motos": ["ktm-450-exc-f", "husqvarna-te-300", "yamaha-wr450f"],
        "cascos": ["agv-pista-gp-rr", "shoei-x-spr-pro", "arai-rx-7v-evo"],
        "ropa": ["alpinestars-mono-gp-plus-v4", "dainese-laguna-seca-5", "rst-tractech-evo-4"],
    }

    def __init__(self, objRepo: Optional[Any] = None) -> None:
        # Conecta el servicio con el repositorio de datos de productos.
        if objRepo is None:
            from datos.producto_repository import ProductoRepository
            objRepo = ProductoRepository()
        self._objRepo = objRepo

    # Compara los productos indicados y arma las caracteristicas comunes para la tabla.
    def comparar(
        self,
        lstProductIds: List[str],
        strCategoria: str = "motos",
        blnAllowDefault: bool = False,
    ) -> Dict[str, Any]:
        if len(lstProductIds) > ComparadorProductos.LIMITE_MAXIMO:
            raise ValueError(
                f"El comparador permite un maximo de {ComparadorProductos.LIMITE_MAXIMO} productos simultaneamente."
            )

        todosProductos = self._objRepo.obtenerTodosComoDict()
        seleccionados = [
            p for p in todosProductos
            if p.get("id") in lstProductIds and p.get("category") == strCategoria
        ]

        if len(seleccionados) == 0 and blnAllowDefault:
            defaultIds = self.DEFAULTS.get(strCategoria, self.DEFAULTS["motos"])
            seleccionados = [p for p in todosProductos if p.get("id") in defaultIds]

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
