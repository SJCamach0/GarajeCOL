"""
=============================================================================
CAPA DE LÓGICA — Clase: Personalización
=============================================================================
Pilar POO: ENCAPSULAMIENTO.

Modela el módulo de personalización y recomendaciones de GarajeCOL.
Registra el perfil, presupuesto, estilo de manejo y nivel de experiencia
del motociclista, recomendando contenido afín y gestionando su historial.
=============================================================================
"""

from typing import List, Dict, Any, Optional
from logica.producto import Producto


class Personalizacion:
    """
    Clase Personalización según el modelado de diseño GarajeCOL.

    ENCAPSULAMIENTO: Atributos privados con nomenclatura estándar (camelCase).
    Controla el historial de consultas de personalización y las preferencias
    del usuario para sugerir productos afines.

    Atributos privados:
        _strConfiguracionUsuario (str): Resumen de configuración del usuario.
        _lstHistorialPreferencias (list): Registro histórico de preferencias evaluadas.
    """

    def __init__(
        self,
        strConfiguracionUsuario: str = "",
        lstHistorialPreferencias: Optional[List[Dict[str, Any]]] = None,
    ) -> None:
        """
        Constructor del módulo de personalización.
        """
        self._strConfiguracionUsuario: str = strConfiguracionUsuario
        self._lstHistorialPreferencias: List[Dict[str, Any]] = lstHistorialPreferencias or []

    # =========================================================================
    # PROPIEDADES EN CAMELCASE (ENCAPSULAMIENTO)
    # =========================================================================

    @property
    def strConfiguracionUsuario(self) -> str:
        """Configuración activa del usuario."""
        return self._strConfiguracionUsuario

    @property
    def lstHistorialPreferencias(self) -> List[Dict[str, Any]]:
        """Historial de preferencias analizadas."""
        return list(self._lstHistorialPreferencias)

    # Aliases de compatibilidad
    configuracion = strConfiguracionUsuario
    historial_preferencias = lstHistorialPreferencias

    # =========================================================================
    # MÉTODOS EN CAMELCASE (REQUISITOS DEL DOCUMENTO DE DISEÑO)
    # =========================================================================

    def personalizarSegunIntereses(
        self, intPresupuesto: int = 45000000, strTipoMoto: str = "enduro", strExperiencia: str = "intermedio"
    ) -> None:
        """
        Registra la configuración de intereses del usuario.

        Parámetros:
            intPresupuesto (int): Presupuesto en pesos colombianos.
            strTipoMoto (str): Tipo de moto buscada.
            strExperiencia (str): Nivel de experiencia del piloto.
        """
        self._strConfiguracionUsuario = (
            f"Presupuesto: {intPresupuesto} COP | Tipo: {strTipoMoto} | Experiencia: {strExperiencia}"
        )
        self._lstHistorialPreferencias.append({
            "presupuesto": intPresupuesto,
            "tipo_moto": strTipoMoto,
            "experiencia": strExperiencia,
        })

    def recomendarContenido(self, objUsuario: Any, lstProductos: Optional[List[Producto]] = None) -> List[Producto]:
        """
        Genera una lista de productos recomendados según los intereses del usuario.

        Parámetros:
            objUsuario: Instancia de Usuario con intereses configurados.
            lstProductos (list, opcional): Colección de productos disponibles.

        Retorna:
            List[Producto]: Productos que coinciden con los intereses del usuario.
        """
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

    def guardarFavoritos(self, objProducto: Any) -> bool:
        """
        Registra en el historial de personalización que un producto fue marcado favorito.

        Parámetros:
            objProducto: Instancia de Producto a registrar.

        Retorna:
            bool: True tras registrar la acción.
        """
        productoId = getattr(objProducto, "intIdProducto", getattr(objProducto, "id_producto", str(objProducto)))
        nombre = getattr(objProducto, "strNombreProducto", getattr(objProducto, "nombre", "Producto"))
        self._lstHistorialPreferencias.append({
            "accion": "guardar_favorito",
            "id": productoId,
            "nombre": nombre,
        })
        return True

    # Aliases snake_case para compatibilidad
    personalizar_segun_intereses = personalizarSegunIntereses
    recomendar_contenido = recomendarContenido
    guardar_favoritos = guardarFavoritos

    def __str__(self) -> str:
        return f"Personalización({self._strConfiguracionUsuario}, {len(self._lstHistorialPreferencias)} interacciones)"
