# Representa el equipo de proteccion como cascos, chaquetas, guantes o monos de cuero.
# Guarda la talla, el material y permite revisar si cumple con normas de seguridad vial.

from typing import Dict, Any
from logica.producto import Producto


class Equipamiento(Producto):
    # Clase para articulos de proteccion del motociclista.

    def __init__(
        self,
        intIdProducto: str,
        strNombreProducto: str,
        strMarcaProducto: str,
        dblPrecioProducto: float,
        strEnlaceTiendaOficial: str,
        strTallaEquipamiento: str = "",
        strMaterialFabricacion: str = "",
        strSubcategoria: str = "cascos",
        **kwargs: Any,
    ) -> None:
        # Envia los datos basicos a Producto y guarda la talla y el material del equipo.
        kwargs.pop("strCategoriaProducto", None)
        super().__init__(
            intIdProducto=intIdProducto,
            strNombreProducto=strNombreProducto,
            strCategoriaProducto=strSubcategoria,
            strMarcaProducto=strMarcaProducto,
            dblPrecioProducto=dblPrecioProducto,
            strEnlaceTiendaOficial=strEnlaceTiendaOficial,
            **kwargs,
        )

        self._strTallaEquipamiento: str = strTallaEquipamiento
        self._strMaterialFabricacion: str = strMaterialFabricacion

    # Propiedades para consultar la talla y el material del accesorio.
    @property
    def strTallaEquipamiento(self) -> str:
        return self._strTallaEquipamiento

    @property
    def strMaterialFabricacion(self) -> str:
        return self._strMaterialFabricacion

    # Nombres faciles para acceder a la talla y al material.
    talla = strTallaEquipamiento
    material_fabricacion = strMaterialFabricacion

    # Muestra los datos de proteccion, materiales y tallas disponibles.
    def revisarEspecificaciones(self) -> str:
        specs = self.dictEspecificaciones
        lineas = [f"Especificaciones de Proteccion — {self.strNombreProducto}"]
        for clave, valor in specs.items():
            lineas.append(f"  • {clave}: {valor}")
        if self._strMaterialFabricacion:
            lineas.append(f"  • Material: {self._strMaterialFabricacion}")
        if self._strTallaEquipamiento:
            lineas.append(f"  • Tallas: {self._strTallaEquipamiento}")
        return "\n".join(lineas)

    # Devuelve el texto con los detalles de seguridad y la tienda oficial.
    def obtenerDetalles(self) -> str:
        detalles = [
            f"{self.strMarcaProducto} {self.strNombreProducto}",
            f"   Precio: {self.strPrecioFormateado}",
            f"   Categoria: {self.strNombreCategoria}",
            f"   {self.strDescripcion}",
        ]
        for clave, valor in self.dictEspecificaciones.items():
            detalles.append(f"   {clave}: {valor}")
        detalles.append(f"   Tienda: {self.strNombreTiendaOficial} — {self.strEnlaceTiendaOficial}")
        return "\n".join(detalles)

    # Comprueba si el casco o prenda cuenta con sellos de certificacion internacional.
    def verificarNivelProteccion(self) -> bool:
        textoSpecs = " ".join(self.dictEspecificaciones.values()).lower()
        normas = ["ece", "dot", "fim", "ce", "homologado", "certificado", "snell"]
        return any(norma in textoSpecs for norma in normas)

    revisar_especificaciones = revisarEspecificaciones
    obtener_detalles = obtenerDetalles
    verificar_nivel_proteccion = verificarNivelProteccion
