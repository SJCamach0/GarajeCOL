# GarajeCOL

Plataforma web para motociclistas en Colombia. Centraliza catálogos técnicos verificados de tiendas y ensambladoras oficiales, permite comparar productos, filtrar según presupuesto y tipo de moto, y consultar la normativa del Código Nacional de Tránsito mediante un asistente por texto.

Desarrollado como prototipo académico en Python con Flask, bajo arquitectura de tres capas (datos, lógica y presentación) y programación orientada a objetos.

---

## Requisitos

- Python 3.10 o superior
- pip (incluido con Python)

Instalar dependencias:

```
pip install flask
```

---

## Iniciar el proyecto

Desde la carpeta raíz `D:\GarajeCOL`:

```
python app.py
```

Luego abrir en el navegador:

```
http://127.0.0.1:5000
```

---

## Estructura del proyecto

```
GarajeCOL/
  app.py                     Punto de entrada principal
  datos/                     Capa de acceso a datos
    productos.json
    traffic_code.json
    producto_repository.py
    traffic_code_repository.py
  logica/                    Capa de logica de negocio y clases POO
    modelos/
      Producto.py
      Motocicleta.py
      Equipamiento.py
      Repuesto.py
      Usuario.py
      Catalogo.py
      ComparadorProductos.py
      Personalizacion.py
      Chatbot.py
      PlataformaWeb.py
    catalogo_service.py
    recomendacion_service.py
    comparador_service.py
    chatbot_service.py
    auth_service.py
  presentacion/              Capa de presentacion (Flask + HTML)
    app.py
    templates/
    static/
```

---

## Modulos de la plataforma

### Inicio de sesion y registro

Rutas `/login` y `/register`. Formulario con validacion de credenciales, opcion de recordar sesion y persistencia del usuario durante la navegacion.

### Catalogos de productos

Rutas `/motos`, `/cascos`, `/ropa-y-accesorios`, `/repuestos`.

Cada catalogo incluye productos reales con fichas tecnicas completas. Los filtros funcionan en tiempo real sin recargar la pagina: por marca, precio maximo en COP, tipo, cilindraje, certificacion y buscador por nombre o referencia.

Productos incluidos (muestra):
- Motos: KTM 450 EXC-F, Husqvarna TE 300, Yamaha WR450F
- Cascos: AGV Pista GP RR, Shoei X-SPR Pro, Arai RX-7V Evo
- Equipamiento: Alpinestars Mono GP Plus V4, Dainese Laguna Seca 5
- Repuestos: Discos Brembo T-Drive 320, Kit Cadena DID ZVM-X, Filtro K&N

### Vista de detalle

Ruta `/producto/<id>`. Galeria con miniaturas, tabla de especificaciones tecnicas, selector de tallas, boton para agregar al comparador y enlace directo a la tienda o distribuidor oficial en Colombia (Auteco, Incolmotos Yamaha, AGV, Shoei, Brembo, entre otros).

### Comparador tecnico

Ruta `/comparador`. Permite comparar hasta 3 productos en paralelo con tabla de especificaciones alineadas. La columna con mejor relacion calidad-precio se resalta automaticamente. Incluye boton para guardar la comparacion y volver al catalogo.

### Filtrar por presupuesto y tipo de moto

Ruta `/personalizacion`. El usuario ingresa su presupuesto maximo en COP mediante un slider y selecciona el tipo de moto que busca (Enduro, Urbana, Pista o Aventura). El sistema devuelve la moto que mejor se ajusta a esos criterios.

### Asistente de normativa vial

Boton flotante accesible desde cualquier pagina. Responde preguntas sobre la normativa colombiana de transito con cita de articulos y fuentes oficiales:

- Ley 769 de 2002 (Codigo Nacional de Transito Terrestre)
- Ley 2251 de 2022 (limites de velocidad - Ley Julian Esteban)
- Resolucion 20203040023385 de 2020 (uso y certificacion del casco)
- SOAT digital, Revision Tecnico Mecanica, chalecos reflectivos, adelantamientos y peajes

Fuentes: MinTransporte, RUNT, Supertransporte, ANSV. Incluye descargo de responsabilidad legal.

### Favoritos

Ruta `/favoritos`. Cualquier producto puede marcarse desde su tarjeta o ficha de detalle. El contador se actualiza en la barra de navegacion. Desde la vista de favoritos se pueden enviar productos directamente al comparador.

---

## Tecnologias

- Backend: Python 3 con Flask
- Frontend: HTML5, Tailwind CSS, JavaScript
- Datos: archivos JSON (`datos/productos.json`, `datos/traffic_code.json`)
- Arquitectura: tres capas (datos / logica / presentacion) con clases POO

---

## Autores

Proyecto academico desarrollado por estudiantes de la institucion.

Santiago Camacho, Samuel Ochoa, Carlos Roldan.
