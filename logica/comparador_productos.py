# Permite comparar hasta 3 productos al mismo tiempo con una tabla frente a frente.
# Revisa las caracteristicas de cada uno y resalta sus diferencias principales.

from typing import List, Dict, Any, Optional
from logica.producto import Producto


class ComparadorProductos:
    # Maneja la lista de productos elegidos para comparar especificaciones.

    LIMITE_MAXIMO: int = 3

    def __init__(self, lstProductosSeleccionados: Optional[List[Producto]] = None) -> None:
        # Guarda la lista de productos a comparar y define el limite maximo de 3 items.
        self._lstProductosSeleccionados: List[Producto] = list(lstProductosSeleccionados) if lstProductosSeleccionados else []
        self._intLimiteComparacion: int = self.LIMITE_MAXIMO

    # Propiedades para consultar los productos seleccionados y el limite permitido.
    @property
    def lstProductosSeleccionados(self) -> List[Producto]:
        return list(self._lstProductosSeleccionados)

    @property
    def intLimiteComparacion(self) -> int:
        return self._intLimiteComparacion

    @property
    def blnEstaVacio(self) -> bool:
        return len(self._lstProductosSeleccionados) == 0

    # Nombres faciles para acceder a los datos del comparador.
    productos_seleccionados = lstProductosSeleccionados
    limite_comparacion = intLimiteComparacion
    esta_vacio = blnEstaVacio

    # Revisa que los productos elegidos tengan especificaciones para poder compararlos.
    def evaluarCaracteristicas(self) -> bool:
        if not self._lstProductosSeleccionados:
            return False
        return all(len(p.dictEspecificaciones) > 0 for p in self._lstProductosSeleccionados)

    # Agrega un producto a la comparacion siempre y cuando no supere el maximo de 3.
    def seleccionarProductos(self, objProducto: Producto) -> bool:
        if len(self._lstProductosSeleccionados) >= self._intLimiteComparacion:
            return False

        idsActuales = [p.intIdProducto for p in self._lstProductosSeleccionados]
        if objProducto.intIdProducto in idsActuales:
            return False

        self._lstProductosSeleccionados.append(objProducto)
        return True

    # Reune todas las caracteristicas tecnicas que se van a comparar en las filas.
    def compararEspecificaciones(self) -> List[str]:
        listaClaves: List[str] = []
        for objProducto in self._lstProductosSeleccionados:
            for clave in objProducto.dictEspecificaciones.keys():
                if clave not in listaClaves:
                    listaClaves.append(clave)
        return listaClaves

    # Genera un texto con las fichas tecnicas de todos los productos seleccionados.
    def generarCuadroComparativo(self) -> str:
        if not self._lstProductosSeleccionados:
            return "No hay productos seleccionados en el comparador."

        lineas = ["CUADRO COMPARATIVO GarajeCOL\n"]
        for i, objProducto in enumerate(self._lstProductosSeleccionados, 1):
            lineas.append(f"--- Producto {i} ---")
            lineas.append(objProducto.obtenerDetalles())
            lineas.append("")
        return "\n".join(lineas)

    # Quita un producto de la comparacion actual.
    def eliminarDeComparacion(self, objProducto: Producto) -> bool:
        idsActuales = [p.intIdProducto for p in self._lstProductosSeleccionados]
        if objProducto.intIdProducto in idsActuales:
            self._lstProductosSeleccionados = [
                p for p in self._lstProductosSeleccionados
                if p.intIdProducto != objProducto.intIdProducto
            ]
            return True
        return False

    # Vacia por completo la lista del comparador.
    def limpiar(self) -> None:
        self._lstProductosSeleccionados.clear()

    evaluar_caracteristicas = evaluarCaracteristicas
    seleccionar_productos = seleccionarProductos
    comparar_especificaciones = compararEspecificaciones
    generar_cuadro_comparativo = generarCuadroComparativo
    eliminar_de_comparacion = eliminarDeComparacion

    # Prepara los datos del comparador para enviarlos a la pagina web.
    def toDict(self, strCategoria: str = "") -> Dict[str, Any]:
        return {
            "category": strCategoria,
            "products": [p.toDict() for p in self._lstProductosSeleccionados],
            "attributes": self.compararEspecificaciones(),
            "max_allowed": self._intLimiteComparacion,
            "is_empty": self.blnEstaVacio,
        }

    to_dict = toDict

    def __str__(self) -> str:
        nombres = [p.strNombreProducto for p in self._lstProductosSeleccionados]
        return f"Comparador({len(nombres)}/{self._intLimiteComparacion}): {', '.join(nombres)}"
