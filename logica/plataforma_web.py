# Modulo que une todo el sistema: conecta el catalogo de productos y los usuarios registrados.
# Controla el registro de nuevas cuentas y la validacion de inicio de sesion.

from typing import List, Optional
from logica.usuario import Usuario
from logica.catalogo import Catalogo


class PlataformaWeb:
    # Representa la plataforma principal GarajeCOL y sus funciones generales.

    def __init__(
        self,
        strNombreSistema: str = "GarajeCOL",
        lstUsuariosRegistrados: Optional[List[Usuario]] = None,
        objCatalogoGeneral: Optional[Catalogo] = None,
    ) -> None:
        # Guarda el nombre del sistema, los usuarios y el catalogo general.
        self._strNombreSistema: str = strNombreSistema
        self._lstUsuariosRegistrados: List[Usuario] = lstUsuariosRegistrados or []
        self._objCatalogoGeneral: Catalogo = objCatalogoGeneral or Catalogo()

    # Propiedades para consultar el nombre, usuarios y catalogo.
    @property
    def strNombreSistema(self) -> str:
        return self._strNombreSistema

    @property
    def lstUsuariosRegistrados(self) -> List[Usuario]:
        return list(self._lstUsuariosRegistrados)

    @property
    def objCatalogoGeneral(self) -> Catalogo:
        return self._objCatalogoGeneral

    nombre_sistema = strNombreSistema
    usuarios_registrados = lstUsuariosRegistrados
    catalogo_general = objCatalogoGeneral

    # Asegura que toda la informacion del catalogo y usuarios este al dia.
    def centralizarInformacion(self) -> None:
        pass

    # Registra un nuevo usuario revisando que el correo no este repetido.
    def registrarUsuario(self, objUsuario: Usuario) -> bool:
        correoNuevo = objUsuario.strCorreoElectronico.lower().strip()
        for u in self._lstUsuariosRegistrados:
            if u.strCorreoElectronico.lower().strip() == correoNuevo:
                return False

        self._lstUsuariosRegistrados.append(objUsuario)
        return True

    # Valida el correo para autorizar el ingreso al sistema.
    def iniciarSesion(self, strCorreo: str, strPassword: str) -> bool:
        correoLimpio = strCorreo.lower().strip()
        for u in self._lstUsuariosRegistrados:
            if u.strCorreoElectronico.lower().strip() == correoLimpio:
                return True
        return False

    centralizar_informacion = centralizarInformacion
    registrar_usuario = registrarUsuario
    iniciar_sesion = iniciarSesion

    def __str__(self) -> str:
        return f"{self._strNombreSistema} ({len(self._lstUsuariosRegistrados)} usuarios, {self._objCatalogoGeneral.intTotalItemsRegistrados} productos)"
