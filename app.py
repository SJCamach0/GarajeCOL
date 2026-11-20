# Archivo principal para iniciar la pagina web de GarajeCOL.
# Se encarga de arrancar el servidor Flask en el computador local.

import sys
import os

# Agrega la carpeta del proyecto para poder encontrar los modulos del sistema.
directorioRaiz = os.path.dirname(os.path.abspath(__file__))
if directorioRaiz not in sys.path:
    sys.path.insert(0, directorioRaiz)

from presentacion.app import app

# Inicia la aplicacion web en el puerto 5000 al ejecutar este archivo.
if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
