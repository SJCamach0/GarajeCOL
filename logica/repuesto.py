"""
=============================================================================
CAPA DE LÓGICA — Subclase: Repuesto
=============================================================================
Pilar POO: HERENCIA y POLIMORFISMO.

Hereda de Producto y añade la verificación de compatibilidad mecánica
con motocicletas específicas (discos, pastillas, bujías, lubricantes, kits).
Sobrescribe obtenerDetalles() y revisarEspecificaciones() respondiendo de
forma polimórfica con los datos mecánicos.
=============================================================================
"""

from typing import Any
from logica.producto import Producto


class Repuesto(Producto):
    """
    Subclase Repuesto que especializa a Producto.

    HERENCIA: Reutiliza nombre, marca, precio, tienda oficial e imagen
    provenientes de la clase padre Producto mediante super().__init__().
    """

    def __init__(
        self,
        intIdProducto: str,
        strNombreProducto: str,
        strMarcaProducto: str,
        dblPrecioProducto: float,
        strEnlaceTiendaOficial: str,
        **kwargs: Any,
    ) -> None:
        """
        Constructor de la clase Repuesto.
        """
        kwargs.pop("strCategoriaProducto", None)
        kwargs.pop("strNombreCategoria", None)
        super().__init__(
            intIdProducto=intIdProducto,
            strNombreProducto=strNombreProducto,
            strCategoriaProducto="repuestos",
            strMarcaProducto=strMarcaProducto,
            dblPrecioProducto=dblPrecioProducto,
            strEnlaceTiendaOficial=strEnlaceTiendaOficial,
            strNombreCategoria="Repuestos",
            **kwargs,
        )

    # =========================================================================
    # POLIMORFISMO: IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS
    # =========================================================================

    def revisarEspecificaciones(self) -> str:
        """
        POLIMORFISMO: Resumen de compatibilidad y especificaciones mecánicas.

        Retorna:
            str: Ficha mecánica del repuesto.
        """
        specs = self.dictEspecificaciones
        lineas = [f"🔧 Especificaciones Mecánicas — {self.strNombreProducto}"]
        for clave, valor in specs.items():
            lineas.append(f"  • {clave}: {valor}")
        return "\n".join(lineas)

    def obtenerDetalles(self) -> str:
        """
        POLIMORFISMO: Retorna la ficha técnica de compatibilidad y rendimiento.

        Retorna:
            str: Especificaciones de compatibilidad mecánica.
        """
        detalles = [
            f"🔧 {self.strMarcaProducto} {self.strNombreProducto}",
            f"   Precio: {self.strPrecioFormateado}",
            f"   {self.strDescripcion}",
        ]
        for clave, valor in self.dictEspecificaciones.items():
            detalles.append(f"   {clave}: {valor}")
        detalles.append(f"   🔗 Tienda: {self.strNombreTiendaOficial} — {self.strEnlaceTiendaOficial}")
        return "\n".join(detalles)

    def verificarCompatibilidad(self, objMotocicleta: Any) -> bool:
        """
        Método exclusivo de Repuesto: verifica si el repuesto es compatible
        con una motocicleta dada analizando marca y modelo en sus especificaciones.

        Parámetros:
            objMotocicleta (Motocicleta): Objeto de motocicleta a comprobar.

        Retorna:
            bool: True si existe compatibilidad declarada, False en caso contrario.
        """
        textoSpecs = " ".join(self.dictEspecificaciones.values()).lower()
        marcaMoto = getattr(objMotocicleta, "strMarcaProducto", getattr(objMotocicleta, "marca", "")).lower()
        nombreMoto = getattr(objMotocicleta, "strNombreProducto", getattr(objMotocicleta, "nombre", "")).lower()

        return marcaMoto in textoSpecs or nombreMoto in textoSpecs

    # Aliases snake_case para compatibilidad
    revisar_especificaciones = revisarEspecificaciones
    obtener_detalles = obtenerDetalles
    verificar_compatibilidad = verificarCompatibilidad
