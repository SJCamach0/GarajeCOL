import os
import json
from flask import Flask, render_template, request, jsonify, session, redirect, url_for

app = Flask(__name__)
app.secret_key = "garajecol_secret_production_key_2026"

DATA_DIR = os.path.join(os.path.dirname(__file__), "data")

def load_products():
    with open(os.path.join(DATA_DIR, "products.json"), "r", encoding="utf-8") as f:
        return json.load(f)

def load_traffic_code():
    with open(os.path.join(DATA_DIR, "traffic_code.json"), "r", encoding="utf-8") as f:
        return json.load(f)

@app.context_processor
def inject_global_data():
    user = session.get("user", None)
    return {
        "current_user": user,
        "is_authenticated": user is not None
    }

# ----------------- PAGE ROUTES -----------------

@app.route("/")
def index():
    products = load_products()
    featured_products = [p for p in products if p.get("featured")]
    return render_template("index.html", featured_products=featured_products)

@app.route("/login")
def login_page():
    return render_template("login.html")

@app.route("/register")
def register_page():
    return render_template("register.html")

@app.route("/motos")
def catalog_motos():
    products = [p for p in load_products() if p["category"] == "motos"]
    return render_template("catalog.html", 
                           category="motos",
                           title="MOTOS PARA IR MÁS LEJOS",
                           subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
                           badge="CATÁLOGO 2026",
                           products=products)

@app.route("/cascos")
def catalog_cascos():
    products = [p for p in load_products() if p["category"] == "cascos"]
    return render_template("catalog.html", 
                           category="cascos",
                           title="CASCOS DE COMPETICIÓN",
                           subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
                           badge="CATÁLOGO 2026",
                           products=products)

@app.route("/ropa-y-accesorios")
def catalog_ropa():
    products = [p for p in load_products() if p["category"] == "ropa"]
    return render_template("catalog.html", 
                           category="ropa",
                           title="ROPA Y ACCESORIOS",
                           subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
                           badge="CATÁLOGO 2026",
                           products=products)

@app.route("/repuestos")
def catalog_repuestos():
    products = [p for p in load_products() if p["category"] == "repuestos"]
    return render_template("catalog.html", 
                           category="repuestos",
                           title="REPUESTOS DE ALTO RENDIMIENTO",
                           subtitle="Equipamiento seleccionado para rendimiento real. Compara especificaciones, disponibilidad y precio.",
                           badge="CATÁLOGO 2026",
                           products=products)

@app.route("/producto/<product_id>")
def product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return redirect(url_for("index"))
    return render_template("detail.html", product=product)

@app.route("/comparador")
def comparator_page():
    category = request.args.get("tipo", "motos")
    if category not in ["motos", "cascos", "ropa"]:
        category = "motos"
    
    titles = {
        "motos": "COMPARADOR DE MOTOS",
        "cascos": "COMPARADOR DE CASCOS",
        "ropa": "COMPARADOR DE EQUIPAMIENTO"
    }
    
    products = [p for p in load_products() if p["category"] == category]
    return render_template("comparator.html", 
                           category=category, 
                           title=titles.get(category),
                           available_products=products)

@app.route("/favoritos")
def favorites_page():
    return render_template("favorites.html")

@app.route("/personalizacion")
def personalization_page():
    return render_template("recommendations.html")

# ----------------- REST API ROUTES -----------------

@app.route("/api/products", methods=["GET"])
def api_products():
    category = request.args.get("category")
    brand = request.args.get("brand")
    q = request.args.get("q", "").lower().strip()
    max_price = request.args.get("max_price", type=int)
    
    products = load_products()
    
    if category:
        products = [p for p in products if p["category"] == category]
    if brand:
        products = [p for p in products if p["brand"].lower() == brand.lower()]
    if max_price:
        products = [p for p in products if p["price"] <= max_price]
    if q:
        products = [
            p for p in products 
            if q in p["name"].lower() or q in p["brand"].lower() or q in p.get("badge", "").lower()
        ]
        
    return jsonify({"products": products, "count": len(products)})

@app.route("/api/products/<product_id>", methods=["GET"])
def api_product_detail(product_id):
    products = load_products()
    product = next((p for p in products if p["id"] == product_id), None)
    if not product:
        return jsonify({"error": "Producto no encontrado"}), 404
    return jsonify(product)

@app.route("/api/compare", methods=["POST"])
def api_compare():
    data = request.get_json() or {}
    product_ids = data.get("ids", [])
    category = data.get("category", "motos")
    allow_default = data.get("allow_default", False)
    
    # Maximum 3 products restriction rule
    if len(product_ids) > 3:
        return jsonify({
            "error": "El comparador permite un máximo de 3 productos simultáneamente.",
            "code": "MAX_LIMIT_EXCEEDED"
        }), 400
        
    all_products = load_products()
    selected_products = [p for p in all_products if p["id"] in product_ids and p["category"] == category]
    
    # If no IDs specified and allow_default is true (e.g. initial landing page demo)
    if len(selected_products) == 0 and allow_default:
        if category == "motos":
            default_ids = ["ktm-450-exc-f", "husqvarna-te-300", "yamaha-wr450f"]
        elif category == "cascos":
            default_ids = ["agv-pista-gp-rr", "shoei-x-spr-pro", "arai-rx-7v-evo"]
        else:
            default_ids = ["alpinestars-mono-gp-plus-v4", "dainese-laguna-seca-5", "rst-tractech-evo-4"]
        selected_products = [p for p in all_products if p["id"] in default_ids]
    
    # Extract common attributes to build comparison table
    specs_keys = []
    for p in selected_products:
        for k in p.get("specs", {}).keys():
            if k not in specs_keys:
                specs_keys.append(k)
                
    return jsonify({
        "category": category,
        "products": selected_products,
        "attributes": specs_keys,
        "max_allowed": 3,
        "is_empty": len(selected_products) == 0
    })

@app.route("/api/recommend", methods=["POST"])
def api_recommend():
    data = request.get_json() or {}
    budget = int(data.get("budget", 45000000))
    bike_type = data.get("bike_type", "enduro").lower()
    experience = data.get("experience", "intermedio").lower()
    
    products = load_products()
    motos = [p for p in products if p["category"] == "motos"]
    
    # 1. Filter by bike type
    motos_of_type = [m for m in motos if m.get("type") == bike_type]
    if not motos_of_type:
        motos_of_type = motos
        
    # 2. Filter within budget
    within_budget = [m for m in motos_of_type if m["price"] <= budget]
    if within_budget:
        # Choose best match (highest spec within budget)
        recommended_moto = sorted(within_budget, key=lambda x: x["price"], reverse=True)[0]
    else:
        # Pick the most affordable in that category
        recommended_moto = sorted(motos_of_type, key=lambda x: x["price"])[0]

    displacement = recommended_moto.get("displacement", 300)
    
    # 3. Intelligent Tiered Gear Selection
    helmets = [p for p in products if p["category"] == "cascos"]
    gear = [p for p in products if p["category"] == "ropa"]
    spares = [p for p in products if p["category"] == "repuestos"]

    if displacement >= 600 or experience == "avanzado":
        gear_tier = "alto"
        safety_alert = {
            "title": "Exigencia de Máxima Protección (Cilindrada Alta / >600 cc)",
            "message": f"Para una máquina de {displacement} cc y alta aceleración, la física vial y la normativa exigen equipamiento de competición o pista: Casco integral FIM/ECE 22.06 de fibra de carbono, protección corporal CE Nivel 2 y frenos de alta resistencia térmica.",
            "level": "max"
        }
        suggested_helmet = next((h for h in helmets if h.get("price_tier") == "alto"), helmets[0])
        suggested_suit = next((g for g in gear if g.get("price_tier") == "alto"), gear[0])
        suggested_spare = next((s for s in spares if "Brembo" in s["name"] or s.get("price_tier") == "alto"), spares[0])
        suggested_gloves = next((g for g in gear if "Guantes" in g["name"] and g.get("price_tier") == "medio"), gear[0])

    elif displacement >= 250 or experience == "intermedio":
        gear_tier = "medio"
        safety_alert = {
            "title": "Protección Equilibrada Carretera / Ciudad (250 cc – 500 cc)",
            "message": f"Para una moto de {displacement} cc, se recomienda protección textil impermeable reforzada con armaduras Nucleon Flex Plus CE Nivel 1/2, guantes de piel con nudillos duros y casco integral homologado ECE 22.06.",
            "level": "med"
        }
        suggested_helmet = next((h for h in helmets if h.get("price_tier") == "medio"), helmets[1])
        suggested_suit = next((g for g in gear if "Chaqueta" in g["name"] and g.get("price_tier") == "medio"), gear[1])
        suggested_spare = next((s for s in spares if "DID" in s["name"] or "Pastillas" in s["name"]), spares[1])
        suggested_gloves = next((g for g in gear if "SMX" in g["name"]), gear[2])

    else:
        gear_tier = "economico"
        safety_alert = {
            "title": "Protección Urbana Diaria Homologada (100 cc – 200 cc)",
            "message": f"Para una cilindrada de {displacement} cc en movilidad urbana, se recomienda equipamiento ágil y transpirable: Casco integral certificado ECE 22.06 (cumplimiento estricto Res. 20203040023385 MinTransporte), chaqueta con reflectivo y guantes contra abrasión.",
            "level": "urban"
        }
        suggested_helmet = next((h for h in helmets if h.get("price_tier") == "economico"), helmets[0])
        suggested_suit = next((g for g in gear if "Chaqueta" in g["name"] and g.get("price_tier") == "economico"), gear[0])
        suggested_spare = next((s for s in spares if "Bujía" in s["name"] or "Motul" in s["name"]), spares[0])
        suggested_gloves = next((g for g in gear if "SH-10" in g["name"]), gear[0])

    return jsonify({
        "moto": recommended_moto,
        "suggested_helmet": suggested_helmet,
        "suggested_suit": suggested_suit,
        "suggested_spare": suggested_spare,
        "suggested_gloves": suggested_gloves,
        "safety_alert": safety_alert,
        "total_budget": budget
    })

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json() or {}
    user_query = data.get("message", "").strip().lower()
    
    if not user_query:
        return jsonify({"error": "Por favor escribe tu consulta sobre las normas de tránsito."}), 400
        
    traffic_data = load_traffic_code()
    topics = traffic_data.get("topics", [])
    disclaimer = traffic_data.get("disclaimer")
    official_sources = traffic_data.get("official_sources", [])
    
    best_topic = None
    best_score = 0
    
    for topic in topics:
        score = 0
        for kw in topic.get("keywords", []):
            if kw in user_query:
                score += 2
        for word in topic.get("title", "").lower().split():
            if len(word) > 3 and word in user_query:
                score += 1
        if score > best_score:
            best_score = score
            best_topic = topic
            
    if best_topic and best_score >= 1:
        rules_text = "\n".join([f"• {r}" for r in best_topic["key_rules"]])
        response_text = (
            f"**{best_topic['title']}**\n\n"
            f"📋 **Fundamento Legal Oficial:** {best_topic['norm']}\n\n"
            f"{best_topic['summary']}\n\n"
            f"**Reglas y consideraciones clave:**\n{rules_text}\n\n"
            f"⚠️ **Sanción aplicable:** {best_topic['sanction']}\n\n"
            f"🔗 **Fuente Oficial:** [{best_topic['norm']}]({best_topic['source_url']})"
        )
        source = {
            "name": "Ministerio de Transporte de Colombia / Código Nacional de Tránsito",
            "norm": best_topic["norm"],
            "url": best_topic["source_url"]
        }
    else:
        response_text = (
            "He analizado tu consulta en la normativa vial colombiana para motociclistas.\n\n"
            "El Código Nacional de Tránsito (Ley 769 de 2002) y la Ley 2251 de 2022 establecen reglas claras para los motociclistas en Colombia:\n\n"
            "• **Casco reglamentario:** Obligatorio, certificado (ECE/DOT), abrochado bajo el mentón y visor cerrado (Res. 20203040023385).\n"
            "• **Prendas reflectivas:** Obligatorias de 6:00 p.m. a 6:00 a.m. (Art. 94 Ley 769).\n"
            "• **Velocidad máxima:** 50 km/h en ciudad y 30 km/h en áreas residenciales/escolares (Ley Julián Esteban).\n"
            "• **Luces encendidas:** 24 horas del día obligatoriamente.\n"
            "• **Documentación:** Licencia A1/A2, Tarjeta de Propiedad, SOAT digital y RTM vigente.\n\n"
            "¿Deseas profundizar en alguna de estas normas o sobre multas específicas?"
        )
        source = {
            "name": "Ministerio de Transporte de Colombia",
            "norm": "Ley 769 de 2002 & Ley 2251 de 2022",
            "url": "https://www.mintransporte.gov.co"
        }
        
    return jsonify({
        "reply": response_text,
        "official_source": source,
        "disclaimer": disclaimer,
        "all_sources": official_sources
    })

# ----------------- AUTH SIMULATION -----------------

@app.route("/api/auth/login", methods=["POST"])
def api_login():
    data = request.get_json() or {}
    email = data.get("email", "").strip()
    password = data.get("password", "")
    
    if not email or not password:
        return jsonify({"error": "Debes ingresar correo electrónico y contraseña."}), 400
        
    user = {
        "email": email,
        "name": email.split("@")[0].capitalize(),
        "created_at": "2026-11-05"
    }
    session["user"] = user
    return jsonify({"success": True, "user": user, "message": f"Bienvenido, {user['name']}!"})

@app.route("/api/auth/register", methods=["POST"])
def api_register():
    data = request.get_json() or {}
    name = data.get("name", "").strip()
    email = data.get("email", "").strip()
    password = data.get("password", "")
    
    if not name or not email or not password:
        return jsonify({"error": "Todos los campos son requeridos."}), 400
        
    user = {
        "email": email,
        "name": name,
        "created_at": "2026-11-05"
    }
    session["user"] = user
    return jsonify({"success": True, "user": user, "message": "Cuenta creada exitosamente."})

@app.route("/api/auth/logout", methods=["POST", "GET"])
def api_logout():
    session.pop("user", None)
    return redirect(url_for("index"))

@app.route("/api/auth/me", methods=["GET"])
def api_me():
    user = session.get("user", None)
    return jsonify({"user": user, "authenticated": user is not None})

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
