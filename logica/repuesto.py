# Representa repuestos y piezas de mantenimiento (frenos, cadenas, bujias, filtros).
# Hereda de Producto y permite revisar si una pieza le sirve a un modelo de moto.

from typing import Any
from logica.producto import Producto


class Repuesto(Producto):
    # Clase para repuestos y componentes mecanicos de motocicletas.

    def __init__(
        self,
        intIdProducto: str,
        strNombreProducto: str,
        strMarcaProducto: str,
        dblPrecioProducto: float,
        strEnlaceTiendaOficial: str,
        **kwargs: Any,
    ) -> None:
        # Envia los datos generales a la clase Producto indicando que es categoria repuestos.
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

    # Devuelve un resumen con las especificaciones del repuesto o componente.
    def revisarEspecificaciones(self) -> str:
        specs = self.dictEspecificaciones
        lineas = [f"Especificaciones Mecanicas — {self.strNombreProducto}"]
        for clave, valor in specs.items():
            lineas.append(f"  • {clave}: {valor}")
        return "\n".join(lineas)

    # Devuelve el texto con los datos tecnicos del repuesto y su tienda oficial.
    def obtenerDetalles(self) -> str:
        detalles = [
            f"{self.strMarcaProducto} {self.strNombreProducto}",
            f"   Precio: {self.strPrecioFormateado}",
            f"   {self.strDescripcion}",
        ]
        for clave, valor in self.dictEspecificaciones.items():
            detalles.append(f"   {clave}: {valor}")
        detalles.append(f"   Tienda: {self.strNombreTiendaOficial} — {self.strEnlaceTiendaOficial}")
        return "\n".join(detalles)

    # Comprueba si el repuesto menciona la marca o el modelo de la moto en su ficha.
    def verificarCompatibilidad(self, objMotocicleta: Any) -> bool:
        textoSpecs = " ".join(self.dictEspecificaciones.values()).lower()
        marcaMoto = getattr(objMotocicleta, "strMarcaProducto", getattr(objMotocicleta, "marca", "")).lower()
        nombreMoto = getattr(objMotocicleta, "strNombreProducto", getattr(objMotocicleta, "nombre", "")).lower()

        return marcaMoto in textoSpecs or nombreMoto in textoSpecs

    revisar_especificaciones = revisarEspecificaciones
    obtener_detalles = obtenerDetalles
    verificar_compatibilidad = verificarCompatibilidad
