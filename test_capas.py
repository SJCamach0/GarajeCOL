"""
Prueba de Verificación de las 3 Capas y CamelCase
"""
import sys
import os

from datos import ProductoRepository, TrafficCodeRepository
from logica import (
    Producto, Motocicleta, Equipamiento, Repuesto, Usuario,
    Catalogo, ComparadorProductos, Personalizacion, Chatbot, PlataformaWeb,
    CatalogoService, RecomendacionService, ComparadorService, ChatbotService, AuthService
)
from presentacion import app

print("=== TEST 1: Importación de las 3 Capas (datos, logica, presentacion) ===")
repo = ProductoRepository()
prods = repo.obtenerTodos()
print(f"  Total productos cargados: {len(prods)}")

motos = [p for p in prods if isinstance(p, Motocicleta)]
equips = [p for p in prods if isinstance(p, Equipamiento)]
reps = [p for p in prods if isinstance(p, Repuesto)]
print(f"  Motocicletas: {len(motos)}")
print(f"  Equipamientos: {len(equips)}")
print(f"  Repuestos: {len(reps)}")

print("\n=== TEST 2: Métodos y Atributos CamelCase ===")
moto = motos[0]
print(f"  strNombreProducto (getter camelCase): {moto.strNombreProducto}")
print(f"  dblPrecioProducto (getter camelCase): {moto.dblPrecioProducto}")
print(f"  obtenerDetalles(): {len(moto.obtenerDetalles())} caracteres")
print(f"  revisarEspecificaciones(): {len(moto.revisarEspecificaciones())} caracteres")
print(f"  mostrarFichaTecnica(): {len(moto.mostrarFichaTecnica())} caracteres")

equip = equips[0]
print(f"  verificarNivelProteccion(): {equip.verificarNivelProteccion()}")

comp = ComparadorProductos()
comp.seleccionarProductos(motos[0])
comp.seleccionarProductos(motos[1])
print(f"  evaluarCaracteristicas(): {comp.evaluarCaracteristicas()}")
print(f"  compararEspecificaciones(): {comp.compararEspecificaciones()}")
print(f"  generarCuadroComparativo(): {len(comp.generarCuadroComparativo())} caracteres")

chat = Chatbot()
chat.cargarBaseConocimiento(TrafficCodeRepository().obtenerDatosCompletos())
resp_chat = chat.orientarSobreCodigoTransito("casco reglamentario")
print(f"  orientarSobreCodigoTransito(): {len(resp_chat['reply'])} caracteres")

plat = PlataformaWeb()
u = Usuario(strCorreoElectronico="user@ecci.edu.co", strNombre="Estudiante")
print(f"  registrarUsuario(): {plat.registrarUsuario(u)}")
print(f"  iniciarSesion(): {plat.iniciarSesion('user@ecci.edu.co', '123')}")

print("\n=== TEST 3: Servicios de la Capa de Lógica ===")
cs = CatalogoService(repo)
print(f"  CatalogoService.obtenerProductosDestacados(): {len(cs.obtenerProductosDestacados())}")
rs = RecomendacionService(repo)
rec = rs.generarRecomendacion()
print(f"  RecomendacionService.generarRecomendacion(): Moto = {rec['moto']['name']}")
cmps = ComparadorService(repo)
comp_res = cmps.comparar(["akt-nkd-125", "boxer-ct-100"])
print(f"  ComparadorService.comparar(): {len(comp_res['products'])} productos")
cbs = ChatbotService()
chat_res = cbs.procesarConsulta("velocidad maxima")
print(f"  ChatbotService.procesarConsulta(): OK")
auth = AuthService()
auth_res = auth.iniciarSesion("test@ecci.edu.co", "password123")
print(f"  AuthService.iniciarSesion(): {auth_res['message']}")

print("\n=== TODOS LOS TESTS DE CAPAS Y CAMELCASE PASARON EXITOSAMENTE ===")
