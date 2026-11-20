# Administra los datos de los usuarios registrados en GarajeCOL.
# Guarda el nombre, correo, fecha de registro y la lista de productos favoritos.

from typing import List, Dict, Any, Optional


class Usuario:
    # Representa la cuenta de un usuario dentro de la aplicacion web.

    def __init__(
        self,
        strPerfilUsuario: str = "",
        lstInteresesUsuario: Optional[List[str]] = None,
        strCorreoElectronico: str = "",
        strContrasenaUsuario: str = "",
        strNombre: str = "",
        strFechaCreacion: str = "",
    ) -> None:
        # Guarda las credenciales y la informacion personal de forma privada.
        self._strPerfilUsuario: str = strPerfilUsuario
        self._lstInteresesUsuario: List[str] = lstInteresesUsuario or []
        self._strCorreoElectronico: str = strCorreoElectronico
        self._strContrasenaUsuario: str = strContrasenaUsuario
        self._strNombre: str = strNombre
        self._strFechaCreacion: str = strFechaCreacion
        self._lstFavoritos: List[str] = []

    # Propiedades para leer los datos del usuario de forma segura.
    @property
    def strPerfilUsuario(self) -> str:
        return self._strPerfilUsuario

    @property
    def lstInteresesUsuario(self) -> List[str]:
        return list(self._lstInteresesUsuario)

    @property
    def strCorreoElectronico(self) -> str:
        return self._strCorreoElectronico

    @property
    def strNombre(self) -> str:
        return self._strNombre

    @property
    def strFechaCreacion(self) -> str:
        return self._strFechaCreacion

    @property
    def lstFavoritos(self) -> List[str]:
        return list(self._lstFavoritos)

    # Nombres faciles para acceder a los datos del usuario.
    perfil = strPerfilUsuario
    intereses = lstInteresesUsuario
    correo_electronico = strCorreoElectronico
    nombre = strNombre
    fecha_creacion = strFechaCreacion
    favoritos = lstFavoritos

    # Actualiza el perfil del usuario de acuerdo a los intereses seleccionados.
    def personalizarSegunIntereses(self) -> None:
        if self._lstInteresesUsuario:
            self._strPerfilUsuario = f"Interesado en: {', '.join(self._lstInteresesUsuario)}"

    # Agrega un producto a la lista de favoritos si no estaba guardado antes.
    def guardarFavoritos(self, objProducto: Any) -> bool:
        productoId = getattr(objProducto, "intIdProducto", getattr(objProducto, "id_producto", str(objProducto)))
        if productoId not in self._lstFavoritos:
            self._lstFavoritos.append(productoId)
            return True
        return False

    # Devuelve la lista de intereses que tiene guardados el usuario.
    def consultarRecomendaciones(self) -> List[str]:
        return list(self._lstInteresesUsuario)

    # Permite cambiar el nombre y los intereses del usuario de forma controlada.
    def modificarPerfil(self, strNombre: Optional[str] = None, lstIntereses: Optional[List[str]] = None) -> bool:
        if strNombre and strNombre.strip():
            self._strNombre = strNombre.strip()
        if lstIntereses is not None:
            self._lstInteresesUsuario = list(lstIntereses)
            self.personalizarSegunIntereses()
        return True

    personalizar_segun_intereses = personalizarSegunIntereses
    guardar_favoritos = guardarFavoritos
    consultar_recomendaciones = consultarRecomendaciones
    modificar_perfil = modificarPerfil

    # Prepara los datos del usuario para enviarlos a la sesion de la pagina web.
    def toDict(self) -> Dict[str, Any]:
        return {
            "email": self._strCorreoElectronico,
            "name": self._strNombre,
            "created_at": self._strFechaCreacion,
        }

    to_dict = toDict

    def __str__(self) -> str:
        return f"Usuario({self._strNombre}, {self._strCorreoElectronico})"
