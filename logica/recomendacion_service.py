"""
=============================================================================
CAPA DE LÓGICA — Servicio: RecomendacionService
=============================================================================
Implementa la lógica del motor de recomendación personalizada de GarajeCOL.
Selecciona la mejor motocicleta dentro del presupuesto y determina el nivel
técnico de protección requerido según cilindrada y experiencia del piloto.
=============================================================================
"""

from typing import Dict, Any, Optional
from logica.personalizacion import Personalizacion


class RecomendacionService:
    """
    Servicio de la lógica de negocio para recomendaciones personalizadas.

    Atributos privados:
        _objRepo: Repositorio para consultar productos.
        _objPersonalizacion (Personalizacion): Modelo de personalización de preferencias.
    """

    def __init__(self, objRepo: Optional[Any] = None) -> None:
        """
        Constructor del servicio de recomendación.
        """
        if objRepo is None:
            from datos.producto_repository import ProductoRepository
            objRepo = ProductoRepository()
        self._objRepo = objRepo
        self._objPersonalizacion: Personalizacion = Personalizacion()

    def generarRecomendacion(
        self,
        intPresupuesto: int = 45000000,
        strTipoMoto: str = "enduro",
        strExperiencia: str = "intermedio",
    ) -> Dict[str, Any]:
        """
        Calcula y selecciona el paquete completo de moto + indumentaria de seguridad
        más apropiado para el presupuesto y nivel del usuario.

        Parámetros:
            intPresupuesto (int): Presupuesto total disponible en pesos colombianos.
            strTipoMoto (str): Estilo de motocicleta ('enduro', 'urbana', 'deportiva', etc.).
            strExperiencia (str): Nivel de manejo ('principiante', 'intermedio', 'avanzado').

        Retorna:
            Dict[str, Any]: Paquete con moto, casco, traje, repuesto, guantes y alerta.
        """
        # Guardar en el modelo de personalización
        self._objPersonalizacion.personalizarSegunIntereses(intPresupuesto, strTipoMoto, strExperiencia)

        productos = self._objRepo.obtenerTodosComoDict()
        motos = [p for p in productos if p.get("category") == "motos"]

        # 1. Filtrar por tipo
        motosDelTipo = [m for m in motos if m.get("type") == strTipoMoto.lower().strip()]
        if not motosDelTipo:
            motosDelTipo = motos

        # 2. Filtrar por presupuesto
        dentroPresupuesto = [m for m in motosDelTipo if m.get("price", 0) <= intPresupuesto]
        if dentroPresupuesto:
            motoElegida = sorted(dentroPresupuesto, key=lambda x: x["price"], reverse=True)[0]
        else:
            motoElegida = sorted(motosDelTipo, key=lambda x: x["price"])[0]

        cilindrada = motoElegida.get("displacement", 300)

        # 3. Selección de indumentaria por niveles de protección
        cascos = [p for p in productos if p.get("category") == "cascos"]
        ropa = [p for p in productos if p.get("category") == "ropa"]
        repuestos = [p for p in productos if p.get("category") == "repuestos"]

        if cilindrada >= 600 or strExperiencia.lower().strip() == "avanzado":
            alerta = self._alertaProteccionMaxima(cilindrada)
            casco = self._seleccionarPorTier(cascos, "alto")
            traje = self._seleccionarPorTier(ropa, "alto")
            repuesto = next((s for s in repuestos if "Brembo" in s["name"] or s.get("price_tier") == "alto"), repuestos[0] if repuestos else {})
            guantes = next((g for g in ropa if "Guantes" in g["name"] and g.get("price_tier") == "medio"), ropa[0] if ropa else {})

        elif cilindrada >= 250 or strExperiencia.lower().strip() == "intermedio":
            alerta = self._alertaProteccionMedia(cilindrada)
            casco = self._seleccionarPorTier(cascos, "medio", 1)
            traje = next((g for g in ropa if "Chaqueta" in g["name"] and g.get("price_tier") == "medio"), ropa[1] if len(ropa) > 1 else ropa[0] if ropa else {})
            repuesto = next((s for s in repuestos if "DID" in s["name"] or "Pastillas" in s["name"]), repuestos[1] if len(repuestos) > 1 else repuestos[0] if repuestos else {})
            guantes = next((g for g in ropa if "SMX" in g["name"]), ropa[2] if len(ropa) > 2 else ropa[0] if ropa else {})

        else:
            alerta = self._alertaProteccionUrbana(cilindrada)
            casco = self._seleccionarPorTier(cascos, "economico")
            traje = next((g for g in ropa if "Chaqueta" in g["name"] and g.get("price_tier") == "economico"), ropa[0] if ropa else {})
            repuesto = next((s for s in repuestos if "Bujía" in s["name"] or "Motul" in s["name"]), repuestos[0] if repuestos else {})
            guantes = next((g for g in ropa if "SH-10" in g["name"]), ropa[0] if ropa else {})

        return {
            "moto": motoElegida,
            "suggested_helmet": casco,
            "suggested_suit": traje,
            "suggested_spare": repuesto,
            "suggested_gloves": guantes,
            "safety_alert": alerta,
            "total_budget": intPresupuesto,
        }

    # Alias snake_case
    generar_recomendacion = generarRecomendacion

    def _seleccionarPorTier(self, lista: list, strTier: str, indiceFallback: int = 0) -> dict:
        """Selecciona un producto que coincida con el tier de precio indicado."""
        return next((item for item in lista if item.get("price_tier") == strTier), lista[indiceFallback] if len(lista) > indiceFallback else {})

    def _alertaProteccionMaxima(self, intCilindrada: int) -> Dict[str, str]:
        return {
            "title": "Exigencia de Máxima Protección (Cilindrada Alta / >600 cc)",
            "message": (
                f"Para una máquina de {intCilindrada} cc y alta aceleración, la física vial y "
                "la normativa exigen equipamiento de pista: Casco integral FIM/ECE 22.06 de "
                "fibra de carbono, protección corporal CE Nivel 2 y frenos de alta resistencia térmica."
            ),
            "level": "max",
        }

    def _alertaProteccionMedia(self, intCilindrada: int) -> Dict[str, str]:
        return {
            "title": "Protección Equilibrada Carretera / Ciudad (250 cc – 500 cc)",
            "message": (
                f"Para una moto de {intCilindrada} cc, se recomienda protección textil "
                "impermeable reforzada con armaduras Nucleon Flex Plus CE Nivel 1/2, "
                "guantes de piel con nudillos duros y casco integral homologado ECE 22.06."
            ),
            "level": "med",
        }

    def _alertaProteccionUrbana(self, intCilindrada: int) -> Dict[str, str]:
        return {
            "title": "Protección Urbana Diaria Homologada (100 cc – 200 cc)",
            "message": (
                f"Para una cilindrada de {intCilindrada} cc en movilidad urbana, se recomienda "
                "equipamiento ágil y transpirable: Casco integral certificado ECE 22.06 "
                "(cumplimiento estricto Res. 20203040023385 MinTransporte), chaqueta reflectiva y guantes."
            ),
            "level": "urban",
        }
