"""
=============================================================================
CAPA DE LÓGICA — Clase: ComparadorProductos
=============================================================================
Pilar POO: POLIMORFISMO y ENCAPSULAMIENTO.

Permite al usuario seleccionar hasta 3 productos y compararlos lado a lado.
Aplica POLIMORFISMO invocando obtenerDetalles() sobre los elementos de la
lista sin importar si son Motocicleta, Equipamiento o Repuesto, logrando
que cada uno aporte su información técnica correspondiente de forma dinámica.
=============================================================================
"""

from typing import List, Dict, Any, Optional
from logica.producto import Producto


class ComparadorProductos:
    """
    Clase ComparadorProductos según el modelado de diseño GarajeCOL.

    POLIMORFISMO: Recorre _lstProductosSeleccionados llamando a
    obtenerDetalles() en cada elemento. No requiere sentencias if/elif
    para discriminar el tipo de producto.

    Atributos privados:
        _lstProductosSeleccionados (list): Lista de productos elegidos.
        _intLimiteComparacion (int): Límite superior de productos (3 por regla de negocio).
    """

    LIMITE_MAXIMO: int = 3

    def __init__(self, lstProductosSeleccionados: Optional[List[Producto]] = None) -> None:
        """
        Constructor del comparador de productos.
        """
        self._lstProductosSeleccionados: List[Producto] = list(lstProductosSeleccionados) if lstProductosSeleccionados else []
        self._intLimiteComparacion: int = self.LIMITE_MAXIMO

    # =========================================================================
    # PROPIEDADES EN CAMELCASE (ENCAPSULAMIENTO)
    # =========================================================================

    @property
    def lstProductosSeleccionados(self) -> List[Producto]:
        """Copia de la lista de productos seleccionados."""
        return list(self._lstProductosSeleccionados)

    @property
    def intLimiteComparacion(self) -> int:
        """Límite máximo permitido de productos en la comparación (3)."""
        return self._intLimiteComparacion

    @property
    def blnEstaVacio(self) -> bool:
        """Indica si el comparador no tiene productos."""
        return len(self._lstProductosSeleccionados) == 0

    # Aliases de compatibilidad
    productos_seleccionados = lstProductosSeleccionados
    limite_comparacion = intLimiteComparacion
    esta_vacio = blnEstaVacio

    # =========================================================================
    # MÉTODOS EN CAMELCASE (REQUISITOS DEL DOCUMENTO DE DISEÑO)
    # =========================================================================

    def evaluarCaracteristicas(self) -> bool:
        """
        Verifica que los productos seleccionados dispongan de especificaciones
        para ser comparados.

        Retorna:
            bool: True si todos cuentan con especificaciones, False en caso contrario.
        """
        if not self._lstProductosSeleccionados:
            return False
        return all(len(p.dictEspecificaciones) > 0 for p in self._lstProductosSeleccionados)

    def seleccionarProductos(self, objProducto: Producto) -> bool:
        """
        Incorpora un producto a la lista de comparación respetando el límite máximo.

        Parámetros:
            objProducto (Producto): Instancia del producto a añadir.

        Retorna:
            bool: True si se añadió exitosamente, False si superaría el límite o ya existe.
        """
        if len(self._lstProductosSeleccionados) >= self._intLimiteComparacion:
            return False

        idsActuales = [p.intIdProducto for p in self._lstProductosSeleccionados]
        if objProducto.intIdProducto in idsActuales:
            return False

        self._lstProductosSeleccionados.append(objProducto)
        return True

    def compararEspecificaciones(self) -> List[str]:
        """
        Consolida la lista de claves técnicas presentes entre todos los productos.

        Retorna:
            List[str]: Nombres de atributos únicos para las filas comparativas.
        """
        listaClaves: List[str] = []
        for objProducto in self._lstProductosSeleccionados:
            for clave in objProducto.dictEspecificaciones.keys():
                if clave not in listaClaves:
                    listaClaves.append(clave)
        return listaClaves

    def generarCuadroComparativo(self) -> str:
        """
        POLIMORFISMO: Recorre los productos e invoca obtenerDetalles()
        en cada uno para generar el reporte unificado de especificaciones.

        Retorna:
            str: Texto formateado con las fichas técnicas comparativas.
        """
        if not self._lstProductosSeleccionados:
            return "No hay productos seleccionados en el comparador."

        lineas = ["═══ CUADRO COMPARATIVO GarajeCOL (POO) ═══\n"]
        for i, objProducto in enumerate(self._lstProductosSeleccionados, 1):
            lineas.append(f"--- Producto {i} ---")
            # Invocación polimórfica: cada subclase responde con su detalle propio
            lineas.append(objProducto.obtenerDetalles())
            lineas.append("")
        return "\n".join(lineas)

    def eliminarDeComparacion(self, objProducto: Producto) -> bool:
        """
        Remueve un producto de la selección activa.

        Parámetros:
            objProducto (Producto): Instancia a remover.

        Retorna:
            bool: True si fue removido, False si no formaba parte de la lista.
        """
        idsActuales = [p.intIdProducto for p in self._lstProductosSeleccionados]
        if objProducto.intIdProducto in idsActuales:
            self._lstProductosSeleccionados = [
                p for p in self._lstProductosSeleccionados
                if p.intIdProducto != objProducto.intIdProducto
            ]
            return True
        return False

    def limpiar(self) -> None:
        """Vacía la lista de comparación."""
        self._lstProductosSeleccionados.clear()

    # Aliases snake_case para compatibilidad
    evaluar_caracteristicas = evaluarCaracteristicas
    seleccionar_productos = seleccionarProductos
    comparar_especificaciones = compararEspecificaciones
    generar_cuadro_comparativo = generarCuadroComparativo
    eliminar_de_comparacion = eliminarDeComparacion

    def toDict(self, strCategoria: str = "") -> Dict[str, Any]:
        """Serializa el estado del comparador para la respuesta JSON."""
        return {
            "category": strCategoria,
            "products": [p.toDict() for p in self._lstProductosSeleccionados],
            "attributes": self.compararEspecificaciones(),
            "max_allowed": self._intLimiteComparacion,
            "is_empty": self.blnEstaVacio,
        }

    # Alias snake_case
    to_dict = toDict

    def __str__(self) -> str:
        nombres = [p.strNombreProducto for p in self._lstProductosSeleccionados]
        return f"Comparador({len(nombres)}/{self._intLimiteComparacion}): {', '.join(nombres)}"
