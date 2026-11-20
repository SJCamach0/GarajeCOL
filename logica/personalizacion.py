# Maneja las preferencias de presupuesto y tipo de moto elegidas por el usuario.
# Guarda el historial de busquedas para recomendar las motos mas adecuadas.

from typing import List, Dict, Any, Optional
from logica.producto import Producto


class Personalizacion:
    # Registra las preferencias del usuario para sugerir productos a su medida.

    def __init__(
        self,
        strConfiguracionUsuario: str = "",
        lstHistorialPreferencias: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        # Guarda la configuracion actual y la lista de preferencias consultadas.
        self._strConfiguracionUsuario: str = strConfiguracionUsuario
        self._lstHistorialPreferencias: List[Dict[str, Any]] = lstHistorialPreferencias or []

    # Propiedades para consultar la configuracion y el historial de busquedas.
    @property
    def strConfiguracionUsuario(self) -> str:
        return self._strConfiguracionUsuario

    @property
    def lstHistorialPreferencias(self) -> List[Dict[str, Any]]:
        return list(self._lstHistorialPreferencias)

    # Nombres faciles para acceder a la configuracion y al historial.
    configuracion = strConfiguracionUsuario
    historial_preferencias = lstHistorialPreferencias

    # Guarda la combinacion de presupuesto y tipo de moto seleccionada por el usuario.
    def personalizarSegunIntereses(
        self, intPresupuesto: int = 45000000, strTipoMoto: str = "enduro", strExperiencia: str = "intermedio"
    ) -> None:
        self._strConfiguracionUsuario = (
            f"Presupuesto: {intPresupuesto} COP | Tipo: {strTipoMoto} | Experiencia: {strExperiencia}"
        )
        self._lstHistorialPreferencias.append({
            "presupuesto": intPresupuesto,
            "tipo_moto": strTipoMoto,
            "experiencia": strExperiencia,
        })

    # Selecciona los productos que coinciden con los gustos y filtros del usuario.
    def recomendarContenido(self, objUsuario: Any, lstProductos: Optional[List[Producto]] = None) -> List[Producto]:
        productos = lstProductos or []
        intereses = getattr(objUsuario, "consultarRecomendaciones", lambda: [])()
        if not intereses:
            return productos[:5]

        recomendados: List[Producto] = []
        for p in productos:
            nombre = p.strNombreProducto.lower()
            for interes in intereses:
                if interes.lower() in nombre:
                    recomendados.append(p)
                    break

        return recomendados if recomendados else productos[:5]

    # Anota en el historial que el usuario marco un producto como favorito.
    def guardarFavoritos(self, objProducto: Any) -> bool:
        productoId = getattr(objProducto, "intIdProducto", getattr(objProducto, "id_producto", str(objProducto)))
        nombre = getattr(objProducto, "strNombreProducto", getattr(objProducto, "nombre", "Producto"))
        self._lstHistorialPreferencias.append({
            "accion": "guardar_favorito",
            "id": productoId,
            "nombre": nombre,
        })
        return True

    personalizar_segun_intereses = personalizarSegunIntereses
    recomendar_contenido = recomendarContenido
    guardar_favoritos = guardarFavoritos

    def __str__(self) -> str:
        return f"Personalizacion({self._strConfiguracionUsuario}, {len(self._lstHistorialPreferencias)} interacciones)"
