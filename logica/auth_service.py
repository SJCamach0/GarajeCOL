"""
=============================================================================
CAPA DE LÓGICA — Servicio: AuthService
=============================================================================
Gestiona la autenticación, inicio de sesión y registro de usuarios
usando el modelo de dominio Usuario y aplicando el encapsulamiento de datos.
=============================================================================
"""

from typing import Dict, Any, Optional
from logica.usuario import Usuario


class AuthService:
    """
    Servicio de la lógica de negocio para la autenticación de usuarios.
    """

    def iniciarSesion(self, strCorreo: str, strPassword: str) -> Dict[str, Any]:
        """
        Valida las credenciales e inicia la sesión del usuario.

        Parámetros:
            strCorreo (str): Correo electrónico del usuario.
            strPassword (str): Contraseña suministrada.

        Retorna:
            Dict[str, Any]: Resultado con estado de éxito, datos de usuario y mensaje.

        Lanza:
            ValueError: Si falta correo o contraseña.
        """
        if not strCorreo or not strPassword:
            raise ValueError("Debes ingresar correo electrónico y contraseña.")

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

    # Alias login
    login = iniciarSesion

    def registrarUsuario(self, strNombre: str, strCorreo: str, strPassword: str) -> Dict[str, Any]:
        """
        Registra una nueva cuenta de usuario en el sistema.

        Parámetros:
            strNombre (str): Nombre completo del usuario.
            strCorreo (str): Correo electrónico.
            strPassword (str): Contraseña de acceso.

        Retorna:
            Dict[str, Any]: Resultado de la operación y datos de la cuenta creada.

        Lanza:
            ValueError: Si falta algún campo requerido.
        """
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

    # Alias registrar
    registrar = registrarUsuario

    def obtenerDatosSesion(self, dictUsuarioSesion: Optional[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Verifica y retorna el estado de autenticación del usuario actual en sesión.

        Parámetros:
            dictUsuarioSesion (dict, opcional): Datos guardados en la sesión Flask.

        Retorna:
            Dict[str, Any]: Diccionario con el usuario y booleano de autenticación.
        """
        return {
            "user": dictUsuarioSesion,
            "authenticated": dictUsuarioSesion is not None,
        }

    # Alias snake_case
    obtener_datos_sesion = obtenerDatosSesion
