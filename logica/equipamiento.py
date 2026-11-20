"""
=============================================================================
CAPA DE LÓGICA — Subclase: Equipamiento
=============================================================================
Pilar POO: HERENCIA y POLIMORFISMO.

Hereda de Producto y añade las características del equipamiento de protección
del motociclista (cascos, chaquetas, guantes, trajes de pista):
talla, material de fabricación y validación de normas de homologación.
Sobrescribe obtenerDetalles() y revisarEspecificaciones() respondiendo de
forma polimórfica con los datos de seguridad y protección.
=============================================================================
"""

from typing import Dict, Any
from logica.producto import Producto


class Equipamiento(Producto):
    """
    Subclase Equipamiento que especializa a Producto.

    HERENCIA: Reutiliza nombre, marca, precio, tienda oficial e imagen
    provenientes de la clase padre Producto mediante super().__init__().

    Atributos privados específicos:
        _strTallaEquipamiento (str): Talla del producto (XS, S, M, L, XL, etc.).
        _strMaterialFabricacion (str): Material principal (Fibra de carbono, cuero, etc.).
    """

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
        """
        Constructor de la clase Equipamiento.

        Invoca al constructor de Producto y asigna los atributos especializados.
        """
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

        # Atributos específicos encapsulados (camelCase)
        self._strTallaEquipamiento: str = strTallaEquipamiento
        self._strMaterialFabricacion: str = strMaterialFabricacion

    # =========================================================================
    # PROPIEDADES EN CAMELCASE (ENCAPSULAMIENTO)
    # =========================================================================

    @property
    def strTallaEquipamiento(self) -> str:
        """Talla del equipamiento."""
        return self._strTallaEquipamiento

    @property
    def strMaterialFabricacion(self) -> str:
        """Material de fabricación del equipamiento."""
        return self._strMaterialFabricacion

    # Aliases de compatibilidad
    talla = strTallaEquipamiento
    material_fabricacion = strMaterialFabricacion

    # =========================================================================
    # POLIMORFISMO: IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS
    # =========================================================================

    def revisarEspecificaciones(self) -> str:
        """
        POLIMORFISMO: Resumen de homologaciones y nivel de protección.

        Retorna:
            str: Ficha de protección y materiales del equipamiento.
        """
        specs = self.dictEspecificaciones
        lineas = [f"🛡️ Especificaciones de Protección — {self.strNombreProducto}"]
        for clave, valor in specs.items():
            lineas.append(f"  • {clave}: {valor}")
        if self._strMaterialFabricacion:
            lineas.append(f"  • Material: {self._strMaterialFabricacion}")
        if self._strTallaEquipamiento:
            lineas.append(f"  • Tallas: {self._strTallaEquipamiento}")
        return "\n".join(lineas)

    def obtenerDetalles(self) -> str:
        """
        POLIMORFISMO: Retorna la ficha técnica de seguridad y homologación.

        Retorna:
            str: Especificaciones de seguridad y certificaciones.
        """
        detalles = [
            f"🛡️ {self.strMarcaProducto} {self.strNombreProducto}",
            f"   Precio: {self.strPrecioFormateado}",
            f"   Categoría: {self.strNombreCategoria}",
            f"   {self.strDescripcion}",
        ]
        for clave, valor in self.dictEspecificaciones.items():
            detalles.append(f"   {clave}: {valor}")
        detalles.append(f"   🔗 Tienda: {self.strNombreTiendaOficial} — {self.strEnlaceTiendaOficial}")
        return "\n".join(detalles)

    def verificarNivelProteccion(self) -> bool:
        """
        Método exclusivo de Equipamiento: comprueba si cuenta con certificaciones
        homologadas reconocidas internacionalmente (ECE 22.06, DOT, FIM, CE).

        Retorna:
            bool: True si cuenta con certificación verificada, False en caso contrario.
        """
        textoSpecs = " ".join(self.dictEspecificaciones.values()).lower()
        normas = ["ece", "dot", "fim", "ce", "homologado", "certificado", "snell"]
        return any(norma in textoSpecs for norma in normas)

    # Aliases snake_case para compatibilidad
    revisar_especificaciones = revisarEspecificaciones
    obtener_detalles = obtenerDetalles
    verificar_nivel_proteccion = verificarNivelProteccion
