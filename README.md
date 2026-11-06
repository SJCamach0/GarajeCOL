# GarajeCOL - Prototipo Oficial para Universidad

Plataforma web centralizada para motociclistas en Colombia, con catálogos verificados de tiendas oficiales, sistema de personalización según presupuesto e interés, comparador técnico multivariable (máx. 3 productos) y asistente inteligente con IA para el Código Nacional de Tránsito y resoluciones del Ministerio de Transporte.

---

## 🚀 Cómo Iniciar el Prototipo

1. **Doble clic en el archivo:**
   ```
   iniciar_servidor.bat
   ```
   O desde tu terminal en la carpeta `D:\GarajeCOL`:
   ```bash
   python app.py
   ```
2. **Abre tu navegador en:**
   ```
   http://127.0.0.1:5000
   ```

---

## 🎯 Módulos Implementados

### 1. Inicio de Sesión y Registro (`/login`, `/register`)
* Diseño dividido idéntico al mockup con banner oscuro, arte neón *"Donde la pasión por rodar se convierte en opinión"* y formulario interactivo.
* Validación de credenciales simulada, recordar sesión y persistencia de usuario.

### 2. Catálogos Oficiales (`/motos`, `/cascos`, `/ropa-y-accesorios`, `/repuestos`)
* **Motos:** KTM 450 EXC-F, Husqvarna TE 300, Yamaha WR450F, etc.
* **Cascos:** AGV Pista GP RR, Shoei X-SPR Pro, Arai RX-7V Evo.
* **Ropa y Equipamiento:** Alpinestars Mono GP Plus V4, Dainese Laguna Seca 5, RST TracTech Evo 4.
* **Repuestos:** Discos Brembo T-Drive 320, Kit Cadena DID ZVM-X, Filtro Racing K&N.
* **Filtros interactivos en tiempo real:** Por marca, precio máximo en COP, tipo, cilindraje, certificación, y buscador por modelo/año/referencia.

### 3. Vistas de Detalle y Enlaces a Tiendas Oficiales (`/producto/<id>`)
* Galería con selector de miniaturas y vista principal ampliada en contenedor oscuro.
* Selector de tallas interactivo.
* Botón **Añadir al Comparador** y botón de **Tienda Oficial / Distribuidor Oficial en Colombia** (enlaces reales a KTM Auteco, Yamaha Incolmotos, AGV, Shoei, Dainese, Brembo).
* Tabla unificada de **Especificaciones Técnicas** idéntica a los mockups.

### 4. Comparador Multivariable (`/comparador`)
* Fiel 100% a los mockups de motos, cascos y equipamiento.
* **Regla estricta:** Límite máximo de 3 productos a la vez (con alertas y validación en API).
* Columna resaltada en verde suave con badge **★ MEJOR VALOR**.
* Botón **Guardar Comparación** y **Volver al Catálogo**.

### 5. Filtrar según Interés y Presupuesto (`/personalizacion`)
* Configuración de presupuesto en COP con slider.
* Selección de modalidad de moto (Enduro, Deportiva/Pista, Urbana, Aventura).
* Generación instantánea de la moto recomendada + equipamiento sugerido (casco certificado, mono de cuero y repuestos).

### 6. Asesor Vial de Tránsito con IA (Chatbot Normativo)
* Botón flotante accesible desde cualquier página.
* Base de conocimiento estructurada de la normativa colombiana:
  * **Ley 769 de 2002** (Código Nacional de Tránsito Terrestre).
  * **Ley 2251 de 2022** (Ley Julián Esteban - Límites de velocidad).
  * **Resolución 20203040023385 de 2020** (Ministerio de Transporte - Uso y certificación del casco).
  * Normas de SOAT digital, Tecnomecánica (RTM), chalecos reflectivos (18:00 a 06:00), adelantamientos y peajes (Ley 787 de 2002).
* Citación explícita de artículos y enlaces a fuentes oficiales (**MinTransporte, RUNT, Supertransporte, ANSV**).
* Descargo de responsabilidad legal visible.

### 7. Mis Favoritos (`/favoritos`)
* Posibilidad de marcar productos con el corazón en cualquier tarjeta o ficha de detalle.
* Contador dinámico en la barra superior.
* Vista dedicada para gestionar productos guardados o enviarlos al comparador.

---

## 🛠️ Tecnologías Utilizadas

* **Backend:** Python 3.14 + Flask (Arquitectura REST modular).
* **Frontend:** HTML5 semántico, Tailwind CSS (CDN), Vanilla JavaScript moderno.
* **Almacenamiento de Datos:** Formato JSON extensible (`data/products.json` y `data/traffic_code.json`).
