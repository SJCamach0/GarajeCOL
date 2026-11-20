# Representa una moto en el sistema, heredando los atributos basicos de Producto.
# Agrega datos propios de una moto como cilindraje, frenos, torque, peso y tipo.

from typing import Dict, Any
from logica.producto import Producto


class Motocicleta(Producto):
    # Clase que guarda las caracteristicas mecanicas y tecnicas de una moto.

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
        # Envia los datos generales a Producto y guarda los datos de la moto.
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

    # Propiedades para consultar los datos tecnicos de la moto.
    @property
    def dblCilindrajeMotocicleta(self) -> float:
        return self._dblCilindrajeMotocicleta

    @property
    def strTipoFrenosMotocicleta(self) -> str:
        return self._strTipoFrenosMotocicleta

    @property
    def dblCapacidadTanque(self) -> float:
        return self._dblCapacidadTanque

    @property
    def dblTorqueMotocicleta(self) -> float:
        return self._dblTorqueMotocicleta

    @property
    def dblPesoMotocicleta(self) -> float:
        return self._dblPesoMotocicleta

    @property
    def intModeloMotocicleta(self) -> int:
        return self._intModeloMotocicleta

    @property
    def strTipo(self) -> str:
        return self._strTipo

    @property
    def strTipoNombre(self) -> str:
        return self._strTipoNombre

    @property
    def intCilindraje(self) -> int:
        return self._intCilindraje

    @property
    def strTierCilindraje(self) -> str:
        return self._strTierCilindraje

    # Nombres faciles para acceder a los datos de la moto.
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

    # Muestra un resumen del motor, frenos y peso de la moto.
    def revisarEspecificaciones(self) -> str:
        specs = self.dictEspecificaciones
        lineas = [f"Especificaciones Tecnicas — {self.strNombreProducto}"]
        lineas.append(f"  • Cilindraje: {specs.get('Cilindraje', f'{self._intCilindraje} cc')}")
        lineas.append(f"  • Tipo de motor: {specs.get('Tipo de motor', 'N/A')}")
        lineas.append(f"  • Frenos: {specs.get('Sistema de frenos', self._strTipoFrenosMotocicleta or 'N/A')}")
        lineas.append(f"  • Torque: {specs.get('Torque', f'{self._dblTorqueMotocicleta} Nm')}")
        lineas.append(f"  • Peso: {specs.get('Peso', f'{self._dblPesoMotocicleta} kg')}")
        return "\n".join(lineas)

    # Devuelve el texto con la informacion completa y tienda de la moto.
    def obtenerDetalles(self) -> str:
        detalles = [
            f"{self.strMarcaProducto} {self.strNombreProducto}",
            f"   Precio: {self.strPrecioFormateado}",
            f"   Tipo: {self._strTipoNombre or self._strTipo}",
            f"   Cilindraje: {self._intCilindraje} cc",
            f"   {self.strDescripcion}",
        ]
        for clave, valor in self.dictEspecificaciones.items():
            detalles.append(f"   {clave}: {valor}")
        detalles.append(f"   Tienda: {self.strNombreTiendaOficial} — {self.strEnlaceTiendaOficial}")
        return "\n".join(detalles)

    # Muestra la ficha tecnica detallada de la moto.
    def mostrarFichaTecnica(self) -> str:
        return self.obtenerDetalles()

    revisar_especificaciones = revisarEspecificaciones
    obtener_detalles = obtenerDetalles
    mostrar_ficha_tecnica = mostrarFichaTecnica

    # Empaqueta la moto en un formato que la pagina web puede mostrar.
    def toDict(self) -> Dict[str, Any]:
        dictBase = super().toDict()
        dictBase.update({
            "type": self._strTipo,
            "type_name": self._strTipoNombre,
            "displacement": self._intCilindraje,
            "displacement_tier": self._strTierCilindraje,
        })
        return dictBase

    to_dict = toDict
