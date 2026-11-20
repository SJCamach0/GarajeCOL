"""
=============================================================================
CAPA DE PRESENTACIÓN — Servidor Web Flask (app.py)
=============================================================================
Responsabilidad ÚNICA: Gestionar la interacción con el usuario a través
de la web (HTTP, renderizado HTML Jinja2 y respuestas JSON para APIs).

ESTRICTA SEPARACIÓN DE CAPAS:
  - NO accede a archivos JSON directamente (tarea de la capa de DATOS).
  - NO ejecuta reglas de filtrado o comparaciones complejas (tarea de LÓGICA).
  - Toda la operación es delegada a los Servicios de la capa 'logica'.

Estructura de 3 Capas:
  ┌────────────────────────────────────────────────────────┐
  │  PRESENTACIÓN (presentacion/app.py + templates + JS)   │
  ├────────────────────────────────────────────────────────┤
  │  LÓGICA (logica/ - Modelos POO y Servicios de Negocio) │
  ├────────────────────────────────────────────────────────┤
  │  DATOS (datos/ - Repositorios y Archivos JSON)         │
  └────────────────────────────────────────────────────────┘
=============================================================================
"""

import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# Importación de la Capa de Lógica de Negocio
from logica.catalogo_service import CatalogoService
from logica.recomendacion_service import RecomendacionService
from logica.comparador_service import ComparadorService
from logica.chatbot_service import ChatbotService
from logica.auth_service import AuthService

# =============================================================================
# INICIALIZACIÓN Y CONFIGURACIÓN DE RUTAS DE PRESENTACIÓN
# =============================================================================

directorioPresentacion = os.path.dirname(os.path.abspath(__file__))
directorioRaiz = os.path.dirname(directorioPresentacion)

# Configuración de carpetas de plantillas y recursos estáticos
rutaTemplates = os.path.join(directorioPresentacion, "templates")
if not os.path.exists(rutaTemplates):
    rutaTemplates = os.path.join(directorioRaiz, "templates")

rutaStatic = os.path.join(directorioPresentacion, "static")
if not os.path.exists(rutaStatic):
    rutaStatic = os.path.join(directorioRaiz, "static")

app = Flask(
    __name__,
    template_folder=rutaTemplates,
    static_folder=rutaStatic,
)
app.secret_key = "garajecol_secret_production_key_2026"

# Inyección de dependencias: instanciación de servicios de la capa de lógica
servicioCatalogo = CatalogoService()
servicioRecomendacion = RecomendacionService()
servicioComparador = ComparadorService()
servicioChatbot = ChatbotService()
servicioAuth = AuthService()


# =============================================================================
# PROCESADOR DE CONTEXTO GLOBAL (Sesión de Usuario)
# =============================================================================

@app.context_processor
def inyectarDatosGlobales():
    """Inyecta el usuario actual en todas las plantillas renderizadas."""
    usuarioSesion = session.get("user", None)
    return {
        "current_user": usuarioSesion,
        "is_authenticated": usuarioSesion is not None,
    }


# =============================================================================
# RUTAS DE PÁGINAS (Vistas HTML de la Capa de Presentación)
# =============================================================================

@app.route("/")
def index():
    """Página de inicio: visualiza productos destacados."""
    productosDestacados = servicioCatalogo.obtenerProductosDestacados()
    return render_template("index.html", featured_products=productosDestacados)


@app.route("/login")
def login_page():
    """Formulario de inicio de sesión."""
    return render_template("login.html")


@app.route("/register")
def register_page():
    """Formulario de registro de usuario."""
    return render_template("register.html")


@app.route("/motos")
def catalog_motos():
    """Catálogo filtrado para la categoría de motocicletas."""
    productos = servicioCatalogo.obtenerProductosPorCategoria("motos")
    return render_template(
        "catalog.html",
        category="motos",
        title="MOTOS PARA IR MÁS LEJOS",
        subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
        badge="CATÁLOGO 2026",
        products=productos,
    )


@app.route("/cascos")
def catalog_cascos():
    """Catálogo filtrado para la categoría de cascos de seguridad."""
    productos = servicioCatalogo.obtenerProductosPorCategoria("cascos")
    return render_template(
        "catalog.html",
        category="cascos",
        title="CASCOS DE COMPETICIÓN",
        subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
        badge="CATÁLOGO 2026",
        products=productos,
    )


@app.route("/ropa-y-accesorios")
def catalog_ropa():
    """Catálogo filtrado para equipamiento, chaquetas, guantes y monos."""
    productos = servicioCatalogo.obtenerProductosPorCategoria("ropa")
    return render_template(
        "catalog.html",
        category="ropa",
        title="ROPA Y ACCESORIOS",
        subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
        badge="CATÁLOGO 2026",
        products=productos,
    )


@app.route("/repuestos")
def catalog_repuestos():
    """Catálogo filtrado para repuestos y componentes de alto rendimiento."""
    productos = servicioCatalogo.obtenerProductosPorCategoria("repuestos")
    return render_template(
        "catalog.html",
        category="repuestos",
        title="REPUESTOS DE ALTO RENDIMIENTO",
        subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
        badge="CATÁLOGO 2026",
        products=productos,
    )


@app.route("/producto/<product_id>")
def product_detail(product_id):
    """Página de detalle técnico individual de un producto."""
    producto = servicioCatalogo.obtenerDetalleProducto(product_id)
    if not producto:
        return redirect(url_for("index"))
    return render_template("detail.html", product=producto)


@app.route("/comparador")
def comparator_page():
    """Página interactiva del comparador de especificaciones (hasta 3 productos)."""
    categoria = request.args.get("tipo", "motos")
    if categoria not in ["motos", "cascos", "ropa"]:
        categoria = "motos"

    titulos = {
        "motos": "COMPARADOR DE MOTOS",
        "cascos": "COMPARADOR DE CASCOS",
        "ropa": "COMPARADOR DE EQUIPAMIENTO",
    }

    productosDisponibles = servicioCatalogo.obtenerProductosPorCategoria(categoria)
    return render_template(
        "comparator.html",
        category=categoria,
        title=titulos.get(categoria),
        available_products=productosDisponibles,
    )


@app.route("/favoritos")
def favorites_page():
    """Página de productos guardados como favoritos por el usuario."""
    return render_template("favorites.html")


@app.route("/personalizacion")
def personalization_page():
    """Página del configurador inteligente de moto y equipamiento según presupuesto."""
    return render_template("recommendations.html")


# =============================================================================
# RUTAS API REST (Consumo asíncrono desde el frontend JS)
# =============================================================================

@app.route("/api/products", methods=["GET"])
def api_products():
    """Endpoint REST: búsqueda y filtrado dinámico de productos."""
    categoria = request.args.get("category")
    marca = request.args.get("brand")
    consulta = request.args.get("q", "").lower().strip()
    precioMaximo = request.args.get("max_price", type=int)

    productos = servicioCatalogo.buscarProductos(
        strCategoria=categoria,
        strMarca=marca,
        strConsulta=consulta,
        intPrecioMaximo=precioMaximo,
    )

    return jsonify({"products": productos, "count": len(productos)})


@app.route("/api/products/<product_id>", methods=["GET"])
def api_product_detail(product_id):
    """Endpoint REST: detalle técnico de un producto en formato JSON."""
    producto = servicioCatalogo.obtenerDetalleProducto(product_id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(producto)


@app.route("/api/compare", methods=["GET", "POST"])
def api_compare():
    """Endpoint REST: compara hasta 3 productos según la regla de negocio."""
    if request.method == "POST":
        datos = request.get_json() or {}
        idsProductos = datos.get("ids", [])
        categoria = datos.get("category", "motos")
        permitirDefault = datos.get("allow_default", False)
    else:
        cadenaIds = request.args.get("ids", "")
        idsProductos = [i.strip() for i in cadenaIds.split(",") if i.strip()]
        categoria = request.args.get("category", "motos")
        permitirDefault = request.args.get("allow_default", "false").lower() == "true"

    try:
        resultado = servicioComparador.comparar(
            lstProductIds=idsProductos,
            strCategoria=categoria,
            blnAllowDefault=permitirDefault,
        )
        return jsonify(resultado)
    except ValueError as error:
        return jsonify({"error": str(error), "code": "MAX_LIMIT_EXCEEDED"}), 400


@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    """Endpoint REST: genera recomendación personalizada por presupuesto y experiencia."""
    datos = request.get_json() or {}
    presupuesto = int(datos.get("budget", 45000000))
    tipoMoto = datos.get("bike_type", "enduro").lower()
    experiencia = datos.get("experience", "intermedio").lower()

    resultado = servicioRecomendacion.generarRecomendacion(
        intPresupuesto=presupuesto,
        strTipoMoto=tipoMoto,
        strExperiencia=experiencia,
    )

    return jsonify(resultado)


@app.route("/api/chat", methods=["POST"])
def api_chat():
    """Endpoint REST: chatbot de orientación normativa de tránsito (Ley 769 / MinTransporte)."""
    datos = request.get_json() or {}
    mensajeUsuario = datos.get("message", "").strip().lower()

    try:
        resultado = servicioChatbot.procesarConsulta(mensajeUsuario)
        return jsonify(resultado)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


# =============================================================================
# RUTAS DE AUTENTICACIÓN (Presentación → AuthService)
# =============================================================================

@app.route("/api/auth/login", methods=["POST"])
def api_login():
    """Endpoint REST: inicio de sesión."""
    datos = request.get_json() or {}
    correo = datos.get("email", "").strip()
    contrasena = datos.get("password", "")

    try:
        resultado = servicioAuth.iniciarSesion(correo, contrasena)
        session["user"] = resultado["user"]
        return jsonify(resultado)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.route("/api/auth/register", methods=["POST"])
def api_register():
    """Endpoint REST: registro de usuario."""
    datos = request.get_json() or {}
    nombre = datos.get("name", "").strip()
    correo = datos.get("email", "").strip()
    contrasena = datos.get("password", "")

    try:
        resultado = servicioAuth.registrarUsuario(nombre, correo, contrasena)
        session["user"] = resultado["user"]
        return jsonify(resultado)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


@app.route("/api/auth/logout", methods=["POST", "GET"])
def api_logout():
    """Cierre de sesión."""
    session.pop("user", None)
    return redirect(url_for("index"))


@app.route("/api/auth/me", methods=["GET"])
def api_me():
    """Verifica estado de la sesión activa."""
    usuarioSesion = session.get("user", None)
    resultado = servicioAuth.obtenerDatosSesion(usuarioSesion)
    return jsonify(resultado)


# =============================================================================
# PUNTO DE ARRANQUE LOCAL
# =============================================================================

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
