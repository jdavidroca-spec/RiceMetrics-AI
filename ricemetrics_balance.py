"""
RiceMetrics AI - Módulo de Balance de Masa y Control de Mermas
Autor: Jesús (Proyecto Diplomado Universidad del Atlántico)
Descripción: Calcula la masa seca, el peso final esperado del lote y las
             alertas de sobre-secado o choque térmico en secado de arroz.
"""

class SecadoraArroz:
    def __init__(self, id_secadora: str, capacidad_ton: float):
        self.id_secadora = id_secadora
        self.capacidad_ton = capacidad_ton

    def calcular_balance_masa(self, masa_inicial_ton: float, humedad_inicial_pct: float, humedad_meta_pct: float = 13.0) -> dict:
        """
        Calcula el balance de materia de un lote de arroz paddy verde.
        - masa_inicial_ton: Peso de entrada en toneladas (t)
        - humedad_inicial_pct: Humedad al entrar a la secadora (%)
        - humedad_meta_pct: Humedad deseada a la salida (por defecto 13.0%)
        """
        if humedad_inicial_pct <= humedad_meta_pct:
            raise ValueError("La humedad inicial debe ser mayor a la humedad meta.")
        
        # 1. Cálculo de Masa Seca (Sólidos)
        masa_solidos_kg = (masa_inicial_ton * 1000) * (1 - (humedad_inicial_pct / 100.0))
        
        # 2. Masa Final Esperada (al alcanzar la humedad meta)
        masa_final_esperada_kg = masa_solidos_kg / (1 - (humedad_meta_pct / 100.0))
        masa_final_esperada_ton = masa_final_esperada_kg / 1000.0
        
        # 3. Agua a evaporar (Pérdida de peso normal por humedad)
        agua_evaporar_kg = (masa_inicial_ton * 1000) - masa_final_esperada_kg
        agua_evaporar_ton = agua_evaporar_kg / 1000.0
        
        return {
            "masa_inicial_ton": masa_inicial_ton,
            "humedad_inicial_pct": humedad_inicial_pct,
            "humedad_meta_pct": humedad_meta_pct,
            "masa_solidos_kg": round(masa_solidos_kg, 2),
            "masa_final_esperada_ton": round(masa_final_esperada_ton, 2),
            "masa_final_esperada_kg": round(masa_final_esperada_kg, 2),
            "agua_evaporar_kg": round(agua_evaporar_kg, 2),
            "agua_evaporar_ton": round(agua_evaporar_ton, 2)
        }

    def diagnostico_operativo(self, balance: dict, temp_aire_celsius: float, tasa_extraccion_pct_hora: float) -> list:
        """
        Genera alertas preventivas para proteger la calidad del grano y evitar mermas.
        """
        alertas = []
        
        # Alerta 1: Temp Excesiva (Choque Térmico)
        if temp_aire_celsius > 45.0:
            alertas.append({
                "nivel": "CRÍTICO",
                "codigo": "ALT_CHOQUE_TERMICO",
                "mensaje": f"Temperatura actual ({temp_aire_celsius}°C) supera el límite seguro (45°C). Alto riesgo de microfisuras y arroz partido."
            })
            
        # Alerta 2: Secado muy rápido (Tensión Mecánica)
        if tasa_extraccion_pct_hora > 2.0:
            alertas.append({
                "nivel": "ADVERTENCIA",
                "codigo": "ALT_TASA_EXTRACCION",
                "mensaje": f"Tasa de secado ({tasa_extraccion_pct_hora}%/h) es muy agresiva. Se recomienda extraer máximo 1.5% - 2.0%/h."
            })
            
        # Alerta 3: Sobre-secado
        if balance["humedad_meta_pct"] < 12.0:
            alertas.append({
                "nivel": "PELIGRO_MERMA",
                "codigo": "ALT_SOBRE_SECADO",
                "mensaje": "La humedad meta está por debajo del 12%. Perderá peso comercial en agua y fragilizará el grano."
            })
            
        if not alertas:
            alertas.append({
                "nivel": "OPTIMO",
                "codigo": "OK_PARAMETROS_SEGUROS",
                "mensaje": "Parámetros de secado dentro de la ventana de rendimiento óptimo."
            })
            
        return alertas


# ==========================================
# EJEMPLO DE EJECUCIÓN (PRUEBA DE CONSOLA)
# ==========================================
if __name__ == "__main__":
    print("--- RICEMETRICS AI: MÓDULO DE BALANCE DE MASA ---")
    secadora1 = SecadoraArroz(id_secadora="SEC-01", capacidad_ton=20.0)
    
    # Datos de entrada del lote (igual a la prueba de AI Studio)
    lote_ingreso = secadora1.calcular_balance_masa(
        masa_inicial_ton=15.0,
        humedad_inicial_pct=24.0,
        humedad_meta_pct=13.0
    )
    
    # Evaluación de condiciones de la máquina
    alertas_lote = secadora1.diagnostico_operativo(
        balance=lote_ingreso,
        temp_aire_celsius=48.0,  # Simulamos temperatura alta para probar alerta
        tasa_extraccion_pct_hora=1.8
    )
    
    # Imprimir Reporte
    print(f"\nLote Procesado en {secadora1.id_secadora}:")
    print(f"• Peso Inicial: {lote_ingreso['masa_inicial_ton']} t ({lote_ingreso['humedad_inicial_pct']}% humedad)")
    print(f"• Sólidos Secos: {lote_ingreso['masa_solidos_kg']} kg")
    print(f"• Peso Esperado a {lote_ingreso['humedad_meta_pct']}%: {lote_ingreso['masa_final_esperada_ton']} t ({lote_ingreso['masa_final_esperada_kg']} kg)")
    print(f"• Agua a Evaporar: {lote_ingreso['agua_evaporar_kg']} kg ({lote_ingreso['agua_evaporar_ton']} t)")
    
    print("\n--- DIAGNÓSTICO Y ALERTAS Y SUGERENCIAS DE PLANTA ---")
    for alt in alertas_lote:
        print(f"[{alt['nivel']}] {alt['codigo']}: {alt['mensaje']}")