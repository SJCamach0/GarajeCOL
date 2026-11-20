# Clase base para todos los productos de la tienda (motos, cascos, ropa y repuestos).
# Guarda las caracteristicas comunes como nombre, marca, precio, fotos y descripcion.

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional


class Producto(ABC):
    # Modelo principal del que heredan las motos, los accesorios y los repuestos.

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
        # Guarda los datos principales del producto en variables privadas para protegerlos.
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

    # Propiedades para consultar los datos del producto de forma segura.
    @property
    def intIdProducto(self) -> str:
        return self._intIdProducto

    @property
    def strNombreProducto(self) -> str:
        return self._strNombreProducto

    @property
    def strCategoriaProducto(self) -> str:
        return self._strCategoriaProducto

    @property
    def strMarcaProducto(self) -> str:
        return self._strMarcaProducto

    @property
    def dblPrecioProducto(self) -> float:
        return self._dblPrecioProducto

    @property
    def strEnlaceTiendaOficial(self) -> str:
        return self._strEnlaceTiendaOficial

    @property
    def strImagen(self) -> str:
        return self._strImagen

    @property
    def strImagenGrande(self) -> str:
        return self._strImagenGrande

    @property
    def lstMiniaturas(self) -> List[str]:
        return list(self._lstMiniaturas)

    @property
    def strNombreTiendaOficial(self) -> str:
        return self._strNombreTiendaOficial

    @property
    def strDescripcion(self) -> str:
        return self._strDescripcion

    @property
    def dictEspecificaciones(self) -> Dict[str, str]:
        return dict(self._dictEspecificaciones)

    @property
    def strNombreCategoria(self) -> str:
        return self._strNombreCategoria

    @property
    def strBadge(self) -> str:
        return self._strBadge

    @property
    def blnDestacado(self) -> bool:
        return self._blnDestacado

    @property
    def blnMejorValor(self) -> bool:
        return self._blnMejorValor

    @property
    def strPrecioFormateado(self) -> str:
        return self._strPrecioFormateado

    @property
    def strTierPrecio(self) -> str:
        return self._strTierPrecio

    # Permite cambiar el precio asegurando que sea un valor valido mayor a cero.
    @dblPrecioProducto.setter
    def dblPrecioProducto(self, dblValor: float) -> None:
        if not isinstance(dblValor, (int, float)) or dblValor < 0:
            raise ValueError("El precio debe ser un numero positivo.")
        self._dblPrecioProducto = float(dblValor)

    # Permite cambiar el nombre asegurando que no quede vacio.
    @strNombreProducto.setter
    def strNombreProducto(self, strValor: str) -> None:
        if not strValor or not strValor.strip():
            raise ValueError("El nombre del producto no puede estar vacio.")
        self._strNombreProducto = strValor.strip()

    # Nombres alternativos para usar las propiedades facilmente en el codigo.
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

    # Metodo que cada tipo de producto debe completar con sus propios datos tecnicos.
    @abstractmethod
    def revisarEspecificaciones(self) -> str:
        pass

    # Metodo que cada producto implementa para mostrar su ficha de informacion completa.
    @abstractmethod
    def obtenerDetalles(self) -> str:
        pass

    revisar_especificaciones = revisarEspecificaciones
    obtener_detalles = obtenerDetalles

    # Convierte la informacion del producto en un diccionario para enviarlo a la pagina web.
    def toDict(self) -> Dict[str, Any]:
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

    to_dict = toDict

    def __str__(self) -> str:
        return f"{self._strMarcaProducto} {self._strNombreProducto} — {self._strPrecioFormateado}"

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__}(id='{self._intIdProducto}', nombre='{self._strNombreProducto}')>"
