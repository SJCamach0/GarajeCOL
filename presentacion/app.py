# Servidor web Flask para la presentacion de GarajeCOL.
# Muestra las paginas en el navegador y responde a las peticiones del usuario.

import os
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

# Servicios de la logica que resuelven las peticiones de la pagina.
from logica.catalogo_service import CatalogoService
from logica.recomendacion_service import RecomendacionService
from logica.comparador_service import ComparadorService
from logica.chatbot_service import ChatbotService
from logica.auth_service import AuthService

# Rutas de las carpetas de pantallas HTML y estilos visuales.
directorioPresentacion = os.path.dirname(os.path.abspath(__file__))
rutaTemplates = os.path.join(directorioPresentacion, "templates")
rutaStatic = os.path.join(directorioPresentacion, "static")

# Inicializacion de la aplicacion Flask con sus carpetas correspondientes.
app = Flask(
    __name__,
    template_folder=rutaTemplates,
    static_folder=rutaStatic,
)
app.secret_key = "garajecol_secret_production_key_2026"

# Instancias de los servicios para consultar datos y aplicar reglas del sistema.
servicioCatalogo = CatalogoService()
servicioRecomendacion = RecomendacionService()
servicioComparador = ComparadorService()
servicioChatbot = ChatbotService()
servicioAuth = AuthService()


# Pasa la informacion del usuario conectado a todas las pantallas de forma automatica.
@app.context_processor
def inyectarDatosGlobales():
    usuarioSesion = session.get("user", None)
    return {
        "current_user": usuarioSesion,
        "is_authenticated": usuarioSesion is not None,
    }


# Muestra la pagina principal con las motos y accesorios destacados.
@app.route("/")
def index():
    productosDestacados = servicioCatalogo.obtenerProductosDestacados()
    return render_template("index.html", featured_products=productosDestacados)


# Muestra el formulario para iniciar sesion en la plataforma.
@app.route("/login")
def login_page():
    return render_template("login.html")


# Muestra la pantalla para crear una cuenta nueva de usuario.
@app.route("/register")
def register_page():
    return render_template("register.html")


# Carga la pagina del catalogo mostrando unicamente las motocicletas.
@app.route("/motos")
def catalog_motos():
    productos = servicioCatalogo.obtenerProductosPorCategoria("motos")
    return render_template(
        "catalog.html",
        category="motos",
        title="MOTOS PARA IR MÁS LEJOS",
        subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
        badge="CATÁLOGO 2026",
        products=productos,
    )


# Carga la pagina del catalogo mostrando unicamente los cascos certificados.
@app.route("/cascos")
def catalog_cascos():
    productos = servicioCatalogo.obtenerProductosPorCategoria("cascos")
    return render_template(
        "catalog.html",
        category="cascos",
        title="CASCOS DE COMPETICIÓN",
        subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
        badge="CATÁLOGO 2026",
        products=productos,
    )


# Carga la pagina del catalogo mostrando chaquetas, monos y guantes.
@app.route("/ropa-y-accesorios")
def catalog_ropa():
    productos = servicioCatalogo.obtenerProductosPorCategoria("ropa")
    return render_template(
        "catalog.html",
        category="ropa",
        title="ROPA Y ACCESORIOS",
        subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
        badge="CATÁLOGO 2026",
        products=productos,
    )


# Carga la pagina del catalogo mostrando repuestos y piezas mecanicas.
@app.route("/repuestos")
def catalog_repuestos():
    productos = servicioCatalogo.obtenerProductosPorCategoria("repuestos")
    return render_template(
        "catalog.html",
        category="repuestos",
        title="REPUESTOS DE ALTO RENDIMIENTO",
        subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
        badge="CATÁLOGO 2026",
        products=productos,
    )


# Muestra la ficha detallada, fotos y tienda oficial de un producto especifico.
@app.route("/producto/<product_id>")
def product_detail(product_id):
    producto = servicioCatalogo.obtenerDetalleProducto(product_id)
    if not producto:
        return redirect(url_for("index"))
    return render_template("detail.html", product=producto)


# Muestra la pantalla del comparador para enfrentar hasta 3 productos.
@app.route("/comparador")
def comparator_page():
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


# Muestra la lista de productos que el usuario guardo como favoritos.
@app.route("/favoritos")
def favorites_page():
    return render_template("favorites.html")


# Muestra el formulario para buscar moto segun el presupuesto y tipo de manejo.
@app.route("/personalizacion")
def personalization_page():
    return render_template("recommendations.html")


# Busca y filtra productos segun los parametros que el usuario escriba en la web.
@app.route("/api/products", methods=["GET"])
def api_products():
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


# Devuelve los datos tecnicos de un producto en formato JSON para el navegador.
@app.route("/api/products/<product_id>", methods=["GET"])
def api_product_detail(product_id):
    producto = servicioCatalogo.obtenerDetalleProducto(product_id)
    if not producto:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(producto)


# Procesa la comparacion de hasta 3 productos y devuelve las columnas alineadas.
@app.route("/api/compare", methods=["GET", "POST"])
def api_compare():
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


# Devuelve la moto que mejor se adapta al presupuesto y tipo seleccionado.
@app.route("/api/recommend", methods=["POST"])
def api_recommend():
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


# Recibe las preguntas del usuario en el chat y responde con las leyes de transito.
@app.route("/api/chat", methods=["POST"])
def api_chat():
    datos = request.get_json() or {}
    mensajeUsuario = datos.get("message", "").strip().lower()

    try:
        resultado = servicioChatbot.procesarConsulta(mensajeUsuario)
        return jsonify(resultado)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


# Recibe el correo y clave del formulario para iniciar sesion del usuario.
@app.route("/api/auth/login", methods=["POST"])
def api_login():
    datos = request.get_json() or {}
    correo = datos.get("email", "").strip()
    contrasena = datos.get("password", "")

    try:
        resultado = servicioAuth.iniciarSesion(correo, contrasena)
        session["user"] = resultado["user"]
        return jsonify(resultado)
    except ValueError as error:
        return jsonify({"error": str(error)}), 400


# Recibe los datos del nuevo usuario para registrarlo en el sistema.
@app.route("/api/auth/register", methods=["POST"])
def api_register():
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


# Cierra la sesion del usuario borrando sus datos de la memoria temporal.
@app.route("/api/auth/logout", methods=["POST", "GET"])
def api_logout():
    session.pop("user", None)
    return redirect(url_for("index"))


# Consulta si hay un usuario con sesion abierta en la pagina.
@app.route("/api/auth/me", methods=["GET"])
def api_me():
    usuarioSesion = session.get("user", None)
    resultado = servicioAuth.obtenerDatosSesion(usuarioSesion)
    return jsonify(resultado)


# Inicia el servidor web si se ejecuta este archivo directamente.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
