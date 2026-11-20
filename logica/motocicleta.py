"""
=============================================================================
CAPA DE LÓGICA — Subclase: Motocicleta
=============================================================================
Pilar POO: HERENCIA y POLIMORFISMO.

Hereda de la clase base Producto todos los atributos y métodos comunes.
Especializa el comportamiento incorporando las propiedades técnicas de las
motocicletas: cilindraje, frenos, torque, peso, capacidad de tanque y modelo.
Sobrescribe obtenerDetalles() y revisarEspecificaciones() respondiendo de
forma polimórfica con los datos mecánicos.
=============================================================================
"""

from typing import Dict, Any
from logica.producto import Producto


class Motocicleta(Producto):
    """
    Subclase Motocicleta que especializa a Producto.

    HERENCIA: Reutiliza nombre, marca, precio, tienda oficial e imagen
    provenientes de la clase padre Producto mediante super().__init__().

    Atributos privados específicos:
        _dblCilindrajeMotocicleta (float): Cilindrada del motor en centímetros cúbicos.
        _strTipoFrenosMotocicleta (str): Tipo y configuración del sistema de frenado.
        _dblCapacidadTanque (float): Capacidad del depósito de combustible en litros/galones.
        _dblTorqueMotocicleta (float): Par motor máximo (Nm).
        _dblPesoMotocicleta (float): Peso en seco o en orden de marcha (kg).
        _intModeloMotocicleta (int): Año modelo de fabricación.
        _strTipo (str): Tipo de moto ('urbana', 'deportiva', 'enduro', 'adventure').
        _strTipoNombre (str): Nombre legible del tipo de moto.
        _intCilindraje (int): Cilindraje entero para filtros y búsquedas.
        _strTierCilindraje (str): Nivel de cilindrada ('bajo', 'medio', 'alto').
    """

    def __init__(
        self,
        intIdProducto: str,
        strNombreProducto: str,
        strMarcaProducto: str,
        dblPrecioProducto: float,
        strEnlaceTiendaOficial: str,
        dblCilindrajeMotocicleta: float = 0.0,
        strTipoFrenosMotocicleta: str = "",
        dblCapacidadTanque: float = 0.0,
        dblTorqueMotocicleta: float = 0.0,
        dblPesoMotocicleta: float = 0.0,
        intModeloMotocicleta: int = 2026,
        strTipo: str = "",
        strTipoNombre: str = "",
        intCilindraje: int = 0,
        strTierCilindraje: str = "",
        **kwargs: Any,
    ) -> None:
        """
        Constructor de la clase Motocicleta.

        Invoca al constructor de Producto y asigna los atributos especializados.
        """
        kwargs.pop("strCategoriaProducto", None)
        kwargs.pop("strNombreCategoria", None)
        super().__init__(
            intIdProducto=intIdProducto,
            strNombreProducto=strNombreProducto,
            strCategoriaProducto="motos",
            strMarcaProducto=strMarcaProducto,
            dblPrecioProducto=dblPrecioProducto,
            strEnlaceTiendaOficial=strEnlaceTiendaOficial,
            strNombreCategoria="Motos",
            **kwargs,
        )

        # Atributos específicos encapsulados (camelCase)
        self._dblCilindrajeMotocicleta: float = dblCilindrajeMotocicleta
        self._strTipoFrenosMotocicleta: str = strTipoFrenosMotocicleta
        self._dblCapacidadTanque: float = dblCapacidadTanque
        self._dblTorqueMotocicleta: float = dblTorqueMotocicleta
        self._dblPesoMotocicleta: float = dblPesoMotocicleta
        self._intModeloMotocicleta: int = intModeloMotocicleta
        self._strTipo: str = strTipo
        self._strTipoNombre: str = strTipoNombre
        self._intCilindraje: int = intCilindraje
        self._strTierCilindraje: str = strTierCilindraje

    # =========================================================================
    # PROPIEDADES EN CAMELCASE (ENCAPSULAMIENTO)
    # =========================================================================

    @property
    def dblCilindrajeMotocicleta(self) -> float:
        """Cilindraje de la motocicleta."""
        return self._dblCilindrajeMotocicleta

    @property
    def strTipoFrenosMotocicleta(self) -> str:
        """Sistema de frenos."""
        return self._strTipoFrenosMotocicleta

    @property
    def dblCapacidadTanque(self) -> float:
        """Capacidad del tanque de combustible."""
        return self._dblCapacidadTanque

    @property
    def dblTorqueMotocicleta(self) -> float:
        """Torque de la motocicleta."""
        return self._dblTorqueMotocicleta

    @property
    def dblPesoMotocicleta(self) -> float:
        """Peso en kg de la motocicleta."""
        return self._dblPesoMotocicleta

    @property
    def intModeloMotocicleta(self) -> int:
        """Año modelo de la motocicleta."""
        return self._intModeloMotocicleta

    @property
    def strTipo(self) -> str:
        """Tipo de moto (clave interna)."""
        return self._strTipo

    @property
    def strTipoNombre(self) -> str:
        """Nombre legible del tipo de moto."""
        return self._strTipoNombre

    @property
    def intCilindraje(self) -> int:
        """Cilindraje como entero para comparaciones."""
        return self._intCilindraje

    @property
    def strTierCilindraje(self) -> str:
        """Tier de cilindraje ('bajo', 'medio', 'alto')."""
        return self._strTierCilindraje

    # Aliases de compatibilidad
    cilindraje = dblCilindrajeMotocicleta
    tipo_frenos = strTipoFrenosMotocicleta
    capacidad_tanque = dblCapacidadTanque
    torque = dblTorqueMotocicleta
    peso = dblPesoMotocicleta
    modelo = intModeloMotocicleta
    tipo = strTipo
    tipo_nombre = strTipoNombre
    displacement = intCilindraje
    displacement_tier = strTierCilindraje

    # =========================================================================
    # POLIMORFISMO: IMPLEMENTACIÓN DE MÉTODOS ABSTRACTOS
    # =========================================================================

    def revisarEspecificaciones(self) -> str:
        """
        POLIMORFISMO: Resumen técnico especializado en el motor y rendimiento.

        Retorna:
            str: Ficha condensada de motor, frenos, torque y peso.
        """
        specs = self.dictEspecificaciones
        lineas = [f"📋 Especificaciones Técnicas — {self.strNombreProducto}"]
        lineas.append(f"  • Cilindraje: {specs.get('Cilindraje', f'{self._intCilindraje} cc')}")
        lineas.append(f"  • Tipo de motor: {specs.get('Tipo de motor', 'N/A')}")
        lineas.append(f"  • Frenos: {specs.get('Sistema de frenos', self._strTipoFrenosMotocicleta or 'N/A')}")
        lineas.append(f"  • Torque: {specs.get('Torque', f'{self._dblTorqueMotocicleta} Nm')}")
        lineas.append(f"  • Peso: {specs.get('Peso', f'{self._dblPesoMotocicleta} kg')}")
        return "\n".join(lineas)

    def obtenerDetalles(self) -> str:
        """
        POLIMORFISMO: Ficha técnica completa de la motocicleta.

        Retorna:
            str: Especificaciones de ingeniería de la moto.
        """
        detalles = [
            f"🏍️ {self.strMarcaProducto} {self.strNombreProducto}",
            f"   Precio: {self.strPrecioFormateado}",
            f"   Tipo: {self._strTipoNombre or self._strTipo}",
            f"   Cilindraje: {self._intCilindraje} cc",
            f"   {self.strDescripcion}",
        ]
        for clave, valor in self.dictEspecificaciones.items():
            detalles.append(f"   {clave}: {valor}")
        detalles.append(f"   🔗 Tienda: {self.strNombreTiendaOficial} — {self.strEnlaceTiendaOficial}")
        return "\n".join(detalles)

    def mostrarFichaTecnica(self) -> str:
        """
        Método exclusivo de la clase Motocicleta para visualizar la ficha técnica completa.

        Retorna:
            str: Detalles técnicos completos de la motocicleta.
        """
        return self.obtenerDetalles()

    # Aliases snake_case para compatibilidad
    revisar_especificaciones = revisarEspecificaciones
    obtener_detalles = obtenerDetalles
    mostrar_ficha_tecnica = mostrarFichaTecnica

    def toDict(self) -> Dict[str, Any]:
        """Extiende la serialización base incorporando atributos de motocicleta."""
        dictBase = super().toDict()
        dictBase.update({
            "type": self._strTipo,
            "type_name": self._strTipoNombre,
            "displacement": self._intCilindraje,
            "displacement_tier": self._strTierCilindraje,
        })
        return dictBase

    # Alias snake_case
    to_dict = toDict
