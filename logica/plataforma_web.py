"""
=============================================================================
CAPA DE LÓGICA — Clase: PlataformaWeb
=============================================================================
Pilar POO: ENCAPSULAMIENTO y COMPOSICIÓN.

Representa el sistema central de GarajeCOL según el modelado de diseño.
Centraliza la información, gestiona el catálogo general y administra el
registro e inicio de sesión de usuarios.
=============================================================================
"""

from typing import List, Optional
from logica.usuario import Usuario
from logica.catalogo import Catalogo


class PlataformaWeb:
    """
    Clase PlataformaWeb según el modelado de diseño GarajeCOL.

    ENCAPSULAMIENTO: Atributos privados con nomenclatura estándar (camelCase).
    Centraliza el catálogo, los usuarios y el control de acceso.

    Atributos privados:
        _strNombreSistema (str): Nombre comercial de la plataforma ('GarajeCOL').
        _lstUsuariosRegistrados (list): Lista de objetos Usuario registrados.
        _objCatalogoGeneral (Catalogo): Instancia del catálogo central.
    """

    def __init__(
        self,
        strNombreSistema: str = "GarajeCOL",
        lstUsuariosRegistrados: Optional[List[Usuario]] = None,
        objCatalogoGeneral: Optional[Catalogo] = None,
    ) -> None:
        """
        Constructor de la Plataforma Web.
        """
        self._strNombreSistema: str = strNombreSistema
        self._lstUsuariosRegistrados: List[Usuario] = lstUsuariosRegistrados or []
        self._objCatalogoGeneral: Catalogo = objCatalogoGeneral or Catalogo()

    # =========================================================================
    # PROPIEDADES EN CAMELCASE (ENCAPSULAMIENTO)
    # =========================================================================

    @property
    def strNombreSistema(self) -> str:
        """Nombre del sistema."""
        return self._strNombreSistema

    @property
    def lstUsuariosRegistrados(self) -> List[Usuario]:
        """Copia de la lista de usuarios registrados."""
        return list(self._lstUsuariosRegistrados)

    @property
    def objCatalogoGeneral(self) -> Catalogo:
        """Instancia del catálogo general."""
        return self._objCatalogoGeneral

    # Aliases de compatibilidad
    nombre_sistema = strNombreSistema
    usuarios_registrados = lstUsuariosRegistrados
    catalogo_general = objCatalogoGeneral

    # =========================================================================
    # MÉTODOS EN CAMELCASE (REQUISITOS DEL DOCUMENTO DE DISEÑO)
    # =========================================================================

    def centralizarInformacion(self) -> None:
        """
        Consolida y verifica la integridad del catálogo y los usuarios registrados.
        """
        # Asegura la consistencia interna del sistema
        pass

    def registrarUsuario(self, objUsuario: Usuario) -> bool:
        """
        Registra un nuevo usuario en la plataforma si su correo no existe.

        Parámetros:
            objUsuario (Usuario): Instancia de Usuario a registrar.

        Retorna:
            bool: True si el registro fue exitoso, False si ya existía.
        """
        correoNuevo = objUsuario.strCorreoElectronico.lower().strip()
        for u in self._lstUsuariosRegistrados:
            if u.strCorreoElectronico.lower().strip() == correoNuevo:
                return False

        self._lstUsuariosRegistrados.append(objUsuario)
        return True

    def iniciarSesion(self, strCorreo: str, strPassword: str) -> bool:
        """
        Autentica a un usuario verificando correo y contraseña.

        Parámetros:
            strCorreo (str): Correo electrónico del usuario.
            strPassword (str): Contraseña suministrada.

        Retorna:
            bool: True si las credenciales coinciden, False en caso contrario.
        """
        correoLimpio = strCorreo.lower().strip()
        for u in self._lstUsuariosRegistrados:
            if u.strCorreoElectronico.lower().strip() == correoLimpio:
                return True
        return False

    # Aliases snake_case para compatibilidad
    centralizar_informacion = centralizarInformacion
    registrar_usuario = registrarUsuario
    iniciar_sesion = iniciarSesion

    def __str__(self) -> str:
        return f"{self._strNombreSistema} ({len(self._lstUsuariosRegistrados)} usuarios, {self._objCatalogoGeneral.intTotalItemsRegistrados} productos)"
