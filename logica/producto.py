"""
=============================================================================
CAPA DE LÓGICA — Clase Abstracta: Producto
=============================================================================
Pilar POO: ABSTRACCIÓN y ENCAPSULAMIENTO.

Define la plantilla base para cualquier artículo que se gestione o visualice
en la plataforma GarajeCOL. Todos los productos comparten identidad, nombre,
categoría, marca, precio y enlace oficial.

El método abstracto obtenerDetalles() fuerza a cada subclase a definir
su propia implementación sin alterar la clase base.
=============================================================================
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class Producto(ABC):
    """
    Clase abstracta Producto.

    Representa el concepto general de producto en la plataforma GarajeCOL.
    Aplica ENCAPSULAMIENTO mediante atributos privados con nomenclatura
    estándar (Hungarian Notation / camelCase) y propiedades con validación.
    Aplica ABSTRACCIÓN definiendo el contrato que todas las subclases deben cumplir.

    Atributos privados:
        _intIdProducto (str): Identificador único del producto.
        _strNombreProducto (str): Nombre comercial del producto.
        _strCategoriaProducto (str): Categoría general ('motos', 'cascos', 'ropa', 'repuestos').
        _strMarcaProducto (str): Fabricante o marca.
        _dblPrecioProducto (float): Precio numérico en pesos colombianos (COP).
        _strEnlaceTiendaOficial (str): URL oficial de la tienda o fabricante.
        _strImagen (str): Ruta a la imagen principal.
        _strImagenGrande (str): Ruta a la imagen en alta resolución.
        _lstMiniaturas (list): Lista de miniaturas complementarias.
        _strNombreTiendaOficial (str): Nombre de la tienda oficial.
        _strDescripcion (str): Descripción detallada del producto.
        _dictEspecificaciones (dict): Especificaciones técnicas clave-valor.
        _strNombreCategoria (str): Nombre legible de la categoría.
        _strBadge (str): Etiqueta informativa visual.
        _blnDestacado (bool): Indicador de producto destacado.
        _blnMejorValor (bool): Indicador de mejor relación calidad/precio.
        _strPrecioFormateado (str): Representación en formato moneda colombiano ($ XX.XXX.XXX).
        _strTierPrecio (str): Nivel de precio ('alto', 'medio', 'economico').
    """

    def __init__(
        self,
        intIdProducto: str,
        strNombreProducto: str,
        strCategoriaProducto: str,
        strMarcaProducto: str,
        dblPrecioProducto: float,
        strEnlaceTiendaOficial: str,
        strImagen: str = "",
        strImagenGrande: str = "",
        lstMiniaturas: Optional[List[str]] = None,
        strNombreTiendaOficial: str = "",
        strDescripcion: str = "",
        dictEspecificaciones: Optional[Dict[str, str]] = None,
        strNombreCategoria: str = "",
        strBadge: str = "",
        blnDestacado: bool = False,
        blnMejorValor: bool = False,
        strPrecioFormateado: str = "",
        strTierPrecio: str = "",
    ) -> None:
        """
        Constructor de la clase base Producto.

        Parámetros:
            intIdProducto (str): Identificador único del producto.
            strNombreProducto (str): Nombre comercial.
            strCategoriaProducto (str): Categoría ('motos', 'cascos', 'ropa', 'repuestos').
            strMarcaProducto (str): Marca del fabricante.
            dblPrecioProducto (float): Precio de venta.
            strEnlaceTiendaOficial (str): Enlace a la tienda oficial.
        """
        # Atributos privados (ENCAPSULAMIENTO)
        self._intIdProducto: str = intIdProducto
        self._strNombreProducto: str = strNombreProducto
        self._strCategoriaProducto: str = strCategoriaProducto
        self._strMarcaProducto: str = strMarcaProducto
        self._dblPrecioProducto: float = float(dblPrecioProducto)
        self._strEnlaceTiendaOficial: str = strEnlaceTiendaOficial
        self._strImagen: str = strImagen
        self._strImagenGrande: str = strImagenGrande
        self._lstMiniaturas: List[str] = lstMiniaturas or []
        self._strNombreTiendaOficial: str = strNombreTiendaOficial
        self._strDescripcion: str = strDescripcion
        self._dictEspecificaciones: Dict[str, str] = dictEspecificaciones or {}
        self._strNombreCategoria: str = strNombreCategoria
        self._strBadge: str = strBadge
        self._blnDestacado: bool = blnDestacado
        self._blnMejorValor: bool = blnMejorValor
        self._strPrecioFormateado: str = strPrecioFormateado
        self._strTierPrecio: str = strTierPrecio

    # =========================================================================
    # PROPIEDADES / GETTERS (ENCAPSULAMIENTO EN CAMELCASE)
    # =========================================================================

    @property
    def intIdProducto(self) -> str:
        """Identificador único del producto."""
        return self._intIdProducto

    @property
    def strNombreProducto(self) -> str:
        """Nombre comercial del producto."""
        return self._strNombreProducto

    @property
    def strCategoriaProducto(self) -> str:
        """Categoría general del producto."""
        return self._strCategoriaProducto

    @property
    def strMarcaProducto(self) -> str:
        """Marca o fabricante del producto."""
        return self._strMarcaProducto

    @property
    def dblPrecioProducto(self) -> float:
        """Precio del producto en COP."""
        return self._dblPrecioProducto

    @property
    def strEnlaceTiendaOficial(self) -> str:
        """URL oficial de la tienda o fabricante."""
        return self._strEnlaceTiendaOficial

    @property
    def strImagen(self) -> str:
        """Ruta a la imagen del producto."""
        return self._strImagen

    @property
    def strImagenGrande(self) -> str:
        """Ruta a la imagen ampliada del producto."""
        return self._strImagenGrande

    @property
    def lstMiniaturas(self) -> List[str]:
        """Copia de la lista de miniaturas."""
        return list(self._lstMiniaturas)

    @property
    def strNombreTiendaOficial(self) -> str:
        """Nombre legible de la tienda oficial."""
        return self._strNombreTiendaOficial

    @property
    def strDescripcion(self) -> str:
        """Descripción detallada del producto."""
        return self._strDescripcion

    @property
    def dictEspecificaciones(self) -> Dict[str, str]:
        """Copia de las especificaciones técnicas."""
        return dict(self._dictEspecificaciones)

    @property
    def strNombreCategoria(self) -> str:
        """Nombre legible de la categoría."""
        return self._strNombreCategoria

    @property
    def strBadge(self) -> str:
        """Etiqueta visual del producto."""
        return self._strBadge

    @property
    def blnDestacado(self) -> bool:
        """Indica si el producto está destacado en inicio."""
        return self._blnDestacado

    @property
    def blnMejorValor(self) -> bool:
        """Indica si tiene la insignia de mejor valor."""
        return self._blnMejorValor

    @property
    def strPrecioFormateado(self) -> str:
        """Precio formateado en moneda colombiana."""
        return self._strPrecioFormateado

    @property
    def strTierPrecio(self) -> str:
        """Nivel o rango de precio ('alto', 'medio', 'economico')."""
        return self._strTierPrecio

    # =========================================================================
    # SETTERS CON VALIDACIÓN (ENCAPSULAMIENTO)
    # =========================================================================

    @dblPrecioProducto.setter
    def dblPrecioProducto(self, dblValor: float) -> None:
        """
        Establece el precio del producto validando que sea positivo.

        Parámetros:
            dblValor (float): Nuevo valor del precio.

        Lanza:
            ValueError: Si el precio es negativo o no numérico.
        """
        if not isinstance(dblValor, (int, float)) or dblValor < 0:
            raise ValueError("El precio debe ser un número positivo.")
        self._dblPrecioProducto = float(dblValor)

    @strNombreProducto.setter
    def strNombreProducto(self, strValor: str) -> None:
        """
        Establece el nombre comercial del producto con validación de no vacío.

        Parámetros:
            strValor (str): Nuevo nombre.

        Lanza:
            ValueError: Si el nombre está vacío.
        """
        if not strValor or not strValor.strip():
            raise ValueError("El nombre del producto no puede estar vacío.")
        self._strNombreProducto = strValor.strip()

    # =========================================================================
    # ALIASES DE PROPIEDADES (Compatibilidad total con snake_case y camelCase)
    # =========================================================================
    id_producto = intIdProducto
    nombre = strNombreProducto
    categoria = strCategoriaProducto
    marca = strMarcaProducto
    precio = dblPrecioProducto
    precio_formateado = strPrecioFormateado
    enlace_tienda_oficial = strEnlaceTiendaOficial
    imagen = strImagen
    imagen_grande = strImagenGrande
    miniaturas = lstMiniaturas
    nombre_tienda_oficial = strNombreTiendaOficial
    descripcion = strDescripcion
    especificaciones = dictEspecificaciones
    nombre_categoria = strNombreCategoria
    badge = strBadge
    es_destacado = blnDestacado
    es_mejor_valor = blnMejorValor
    tier_precio = strTierPrecio

    # =========================================================================
    # MÉTODOS ABSTRACTOS (ABSTRACCIÓN)
    # =========================================================================

    @abstractmethod
    def revisarEspecificaciones(self) -> str:
        """
        ABSTRACCIÓN: Retorna un resumen de las especificaciones técnicas.
        Cada subclase debe implementar su propia lógica especializada.

        Retorna:
            str: Resumen formateado de especificaciones.
        """
        pass

    @abstractmethod
    def obtenerDetalles(self) -> str:
        """
        ABSTRACCIÓN y POLIMORFISMO: Retorna la ficha técnica detallada del producto.
        Cada subclase responde con sus campos distintivos.

        Retorna:
            str: Detalle completo del producto.
        """
        pass

    # Aliases snake_case para compatibilidad
    revisar_especificaciones = revisarEspecificaciones
    obtener_detalles = obtenerDetalles

    # =========================================================================
    # SERIALIZACIÓN
    # =========================================================================

    def toDict(self) -> Dict[str, Any]:
        """
        Convierte el objeto en un diccionario listo para consumo de la API JSON.

        Retorna:
            Dict[str, Any]: Representación estructurada del producto.
        """
        return {
            "id": self._intIdProducto,
            "name": self._strNombreProducto,
            "category": self._strCategoriaProducto,
            "category_name": self._strNombreCategoria,
            "brand": self._strMarcaProducto,
            "price": self._dblPrecioProducto,
            "price_formatted": self._strPrecioFormateado,
            "image": self._strImagen,
            "image_large": self._strImagenGrande,
            "thumbnails": self._lstMiniaturas,
            "official_url": self._strEnlaceTiendaOficial,
            "official_store_name": self._strNombreTiendaOficial,
            "description": self._strDescripcion,
            "specs": self._dictEspecificaciones,
            "badge": self._strBadge,
            "featured": self._blnDestacado,
            "best_value": self._blnMejorValor,
            "price_tier": self._strTierPrecio,
        }

    # Alias snake_case
    to_dict = toDict

    def __str__(self) -> str:
        return f"{self._strMarcaProducto} {self._strNombreProducto} — {self._strPrecioFormateado}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id='{self._intIdProducto}', nombre='{self._strNombreProducto}')>"
