"""
=============================================================================
Punto de Entrada Principal — GarajeCOL
=============================================================================
Este archivo actúa como lanzador principal del sistema, importando y
ejecutando la Capa de Presentación (presentacion.app).

Arquitectura de 3 Capas:
  - datos/        : Repositorios y archivos JSON de persistencia.
  - logica/       : Modelos de dominio POO y servicios de negocio.
  - presentacion/ : Controladores Flask, rutas web, plantillas y assets.
=============================================================================
"""

import sys
import os

# Asegurar que el directorio raíz de GarajeCOL esté en sys.path
directorioRaiz = os.path.dirname(os.path.abspath(__file__))
if directorioRaiz not in sys.path:
    sys.path.insert(0, directorioRaiz)

from presentacion.app import app

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
