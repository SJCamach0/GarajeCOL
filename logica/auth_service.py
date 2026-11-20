# Servicio que controla el acceso de usuarios, inicio de sesion y registro.
# Comprueba que los campos no esten vacios y crea la sesion en el sistema.

from typing import Dict, Any, Optional
from logica.usuario import Usuario


class AuthService:
    # Servicio que administra la seguridad y credenciales de las cuentas de usuario.

    # Comprueba que se haya ingresado correo y contrasena para iniciar sesion.
    def iniciarSesion(self, strCorreo: str, strPassword: str) -> Dict[str, Any]:
        if not strCorreo or not strPassword:
            raise ValueError("Debes ingresar correo electronico y contrasena.")

        objUsuario = Usuario(
            strCorreoElectronico=strCorreo.strip(),
            strNombre=strCorreo.split("@")[0].capitalize(),
            strContrasenaUsuario=strPassword,
            strFechaCreacion="2026-11-05",
        )

        return {
            "success": True,
            "user": objUsuario.toDict(),
            "message": f"Bienvenido, {objUsuario.strNombre}!",
        }

    login = iniciarSesion

    # Valida los datos y registra una nueva cuenta en la plataforma.
    def registrarUsuario(self, strNombre: str, strCorreo: str, strPassword: str) -> Dict[str, Any]:
        if not strNombre or not strCorreo or not strPassword:
            raise ValueError("Todos los campos son requeridos.")

        objUsuario = Usuario(
            strCorreoElectronico=strCorreo.strip(),
            strNombre=strNombre.strip(),
            strContrasenaUsuario=strPassword,
            strFechaCreacion="2026-11-05",
        )

        return {
            "success": True,
            "user": objUsuario.toDict(),
            "message": "Cuenta creada exitosamente.",
        }

    registrar = registrarUsuario

    # Revisa si hay un usuario conectado actualmente en la pagina web.
    def obtenerDatosSesion(self, dictUsuarioSesion: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        return {
            "user": dictUsuarioSesion,
            "authenticated": dictUsuarioSesion is not None,
        }

    obtener_datos_sesion = obtenerDatosSesion
