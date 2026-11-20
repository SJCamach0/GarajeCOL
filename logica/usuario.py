"""
=============================================================================
CAPA DE LÓGICA — Clase: Usuario
=============================================================================
Pilar POO: ENCAPSULAMIENTO.

Representa a los usuarios registrados en la plataforma GarajeCOL.
Gestiona de forma segura los datos personales, intereses, perfil
y productos favoritos mediante métodos y atributos privados.
=============================================================================
"""

from typing import List, Dict, Any, Optional


class Usuario:
    """
    Clase Usuario según el modelado de diseño GarajeCOL.

    ENCAPSULAMIENTO: Atributos privados con nomenclatura estándar (camelCase).
    No permite modificar credenciales o intereses directamente desde el exterior,
    sino a través de sus métodos públicos con validación.

    Atributos privados:
        _strPerfilUsuario (str): Descripción o nivel del perfil del usuario.
        _lstInteresesUsuario (list): Lista de intereses (categorías, marcas, estilos).
        _strCorreoElectronico (str): Dirección de correo electrónico única.
        _strContrasenaUsuario (str): Contraseña segura del usuario.
        _strNombre (str): Nombre del usuario.
        _strFechaCreacion (str): Fecha de registro en el sistema.
        _lstFavoritos (list): Lista de identificadores de productos guardados.
    """

    def __init__(
        self,
        strPerfilUsuario: str = "",
        lstInteresesUsuario: Optional[List[str]] = None,
        strCorreoElectronico: str = "",
        strContrasenaUsuario: str = "",
        strNombre: str = "",
        strFechaCreacion: str = "",
    ) -> None:
        """
        Constructor de la clase Usuario.
        """
        self._strPerfilUsuario: str = strPerfilUsuario
        self._lstInteresesUsuario: List[str] = lstInteresesUsuario or []
        self._strCorreoElectronico: str = strCorreoElectronico
        self._strContrasenaUsuario: str = strContrasenaUsuario
        self._strNombre: str = strNombre
        self._strFechaCreacion: str = strFechaCreacion
        self._lstFavoritos: List[str] = []

    # =========================================================================
    # PROPIEDADES EN CAMELCASE (ENCAPSULAMIENTO)
    # =========================================================================

    @property
    def strPerfilUsuario(self) -> str:
        """Perfil actual del usuario."""
        return self._strPerfilUsuario

    @property
    def lstInteresesUsuario(self) -> List[str]:
        """Copia de la lista de intereses declarados."""
        return list(self._lstInteresesUsuario)

    @property
    def strCorreoElectronico(self) -> str:
        """Correo electrónico del usuario."""
        return self._strCorreoElectronico

    @property
    def strNombre(self) -> str:
        """Nombre del usuario."""
        return self._strNombre

    @property
    def strFechaCreacion(self) -> str:
        """Fecha de registro."""
        return self._strFechaCreacion

    @property
    def lstFavoritos(self) -> List[str]:
        """Copia de los favoritos guardados."""
        return list(self._lstFavoritos)

    # Aliases de compatibilidad
    perfil = strPerfilUsuario
    intereses = lstInteresesUsuario
    correo_electronico = strCorreoElectronico
    nombre = strNombre
    fecha_creacion = strFechaCreacion
    favoritos = lstFavoritos

    # =========================================================================
    # MÉTODOS EN CAMELCASE (REQUISITOS DEL DOCUMENTO DE DISEÑO)
    # =========================================================================

    def personalizarSegunIntereses(self) -> None:
        """
        Actualiza el perfil interno según los intereses registrados en el usuario.
        """
        if self._lstInteresesUsuario:
            self._strPerfilUsuario = f"Interesado en: {', '.join(self._lstInteresesUsuario)}"

    def guardarFavoritos(self, objProducto: Any) -> bool:
        """
        Añade un producto a la lista de favoritos si no está ya presente.

        Parámetros:
            objProducto: Instancia de Producto o id del producto.

        Retorna:
            bool: True si se añadió exitosamente, False si ya existía.
        """
        productoId = getattr(objProducto, "intIdProducto", getattr(objProducto, "id_producto", str(objProducto)))
        if productoId not in self._lstFavoritos:
            self._lstFavoritos.append(productoId)
            return True
        return False

    def consultarRecomendaciones(self) -> List[str]:
        """
        Consulta los criterios que orientan las recomendaciones personalizadas.

        Retorna:
            List[str]: Lista de intereses activos del usuario.
        """
        return list(self._lstInteresesUsuario)

    def modificarPerfil(self, strNombre: Optional[str] = None, lstIntereses: Optional[List[str]] = None) -> bool:
        """
        Modifica los datos del perfil de forma controlada y validada.

        Parámetros:
            strNombre (str, opcional): Nuevo nombre.
            lstIntereses (list, opcional): Nueva lista de intereses.

        Retorna:
            bool: True si la modificación fue exitosa.
        """
        if strNombre and strNombre.strip():
            self._strNombre = strNombre.strip()
        if lstIntereses is not None:
            self._lstInteresesUsuario = list(lstIntereses)
            self.personalizarSegunIntereses()
        return True

    # Aliases snake_case para compatibilidad
    personalizar_segun_intereses = personalizarSegunIntereses
    guardar_favoritos = guardarFavoritos
    consultar_recomendaciones = consultarRecomendaciones
    modificar_perfil = modificarPerfil

    def toDict(self) -> Dict[str, Any]:
        """Serializa los datos seguros del usuario excluyendo la contraseña."""
        return {
            "email": self._strCorreoElectronico,
            "name": self._strNombre,
            "created_at": self._strFechaCreacion,
        }

    # Alias snake_case
    to_dict = toDict

    def __str__(self) -> str:
        return f"Usuario({self._strNombre}, {self._strCorreoElectronico})"
