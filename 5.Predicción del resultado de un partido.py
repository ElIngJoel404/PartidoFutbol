import numpy as np
from collections import Counter
import random

class SimuladorPartido:
    def __init__(self, nombre_equipo_local, nombre_equipo_visitante):
        self.nombre_local = nombre_equipo_local
        self.nombre_visitante = nombre_equipo_visitante
        
    def calcular_goles_esperados(self, posesion, tiros_promedio, efectividad):
        """
        Calcula los goles esperados usando las estadísticas del equipo
        
        Parámetros:
        - posesion: Porcentaje de posesión del balón (0-100)
        - tiros_promedio: Promedio de tiros al arco por partido
        - efectividad: Porcentaje de efectividad en goles (0-100)
        """
        # Factor de posesión (mayor posesión = más oportunidades)
        factor_posesion = posesion / 100
        
        # Factor de efectividad
        factor_efectividad = efectividad / 100
        
        # Cálculo de goles esperados (lambda para Poisson)
        goles_esperados = tiros_promedio * factor_efectividad * (0.5 + 0.5 * factor_posesion)
        
        return max(0.1, goles_esperados)  # Mínimo 0.1 para evitar cero
    
    def simular_goles(self, goles_esperados):
        """
        Simula la cantidad de goles usando distribución de Poisson
        """
        return np.random.poisson(goles_esperados)
    
    def simular_partido(self, goles_esperados_local, goles_esperados_visitante):
        """
        Simula un partido completo
        Retorna: (goles_local, goles_visitante, resultado)
        """
        goles_local = self.simular_goles(goles_esperados_local)
        goles_visitante = self.simular_goles(goles_esperados_visitante)
        
        if goles_local > goles_visitante:
            resultado = "victoria_local"
        elif goles_local < goles_visitante:
            resultado = "victoria_visitante"
        else:
            resultado = "empate"
            
        return goles_local, goles_visitante, resultado
    
    def simulacion_monte_carlo(self, goles_esperados_local, goles_esperados_visitante, 
                                num_simulaciones=100):
        """
        Ejecuta múltiples simulaciones usando Monte Carlo
        """
        resultados = []
        marcadores = []
        
        print(f"\n{'='*60}")
        print(f"SIMULACIÓN MONTE CARLO - {num_simulaciones:,} iteraciones")
        print(f"{'='*60}")
        
        for i in range(num_simulaciones):
            goles_local, goles_visitante, resultado = self.simular_partido(
                goles_esperados_local, goles_esperados_visitante
            )
            resultados.append(resultado)
            marcadores.append((goles_local, goles_visitante))
        
        return resultados, marcadores
    
    def analizar_resultados(self, resultados, marcadores):
        """
        Analiza los resultados de las simulaciones
        """
        total_simulaciones = len(resultados)
        
        # Contar resultados
        victorias_local = resultados.count("victoria_local")
        victorias_visitante = resultados.count("victoria_visitante")
        empates = resultados.count("empate")
        
        # Calcular porcentajes
        porcentaje_victoria_local = (victorias_local / total_simulaciones) * 100
        porcentaje_victoria_visitante = (victorias_visitante / total_simulaciones) * 100
        porcentaje_empate = (empates / total_simulaciones) * 100
        
        # Encontrar marcadores más probables
        contador_marcadores = Counter(marcadores)
        marcadores_mas_comunes = contador_marcadores.most_common(5)
        
        return {
            'victorias_local': victorias_local,
            'victorias_visitante': victorias_visitante,
            'empates': empates,
            'porcentaje_victoria_local': porcentaje_victoria_local,
            'porcentaje_victoria_visitante': porcentaje_victoria_visitante,
            'porcentaje_empate': porcentaje_empate,
            'marcadores_mas_comunes': marcadores_mas_comunes,
            'total_simulaciones': total_simulaciones
        }
    
    def mostrar_resultados(self, analisis, goles_esp_local, goles_esp_visitante):
        """
        Muestra los resultados de forma legible en consola
        """
        print(f"\n{'='*60}")
        print(f"PARTIDO: {self.nombre_local} vs {self.nombre_visitante}")
        print(f"{'='*60}")
        
        print(f"\nGOLES ESPERADOS (λ - Lambda de Poisson):")
        print(f"   {self.nombre_local}: {goles_esp_local:.2f} goles")
        print(f"   {self.nombre_visitante}: {goles_esp_visitante:.2f} goles")
        
        print(f"\n{'='*60}")
        print(f"RESULTADOS DE LA SIMULACIÓN")
        print(f"{'='*60}")
        print(f"Total de simulaciones: {analisis['total_simulaciones']:,}\n")
        
        print(f" PROBABILIDADES DE RESULTADO:")
        print(f"   Victoria {self.nombre_local:20s}: {analisis['porcentaje_victoria_local']:6.2f}% ({analisis['victorias_local']:,} veces)")
        print(f"   Empate{' '*26}: {analisis['porcentaje_empate']:6.2f}% ({analisis['empates']:,} veces)")
        print(f"   Victoria {self.nombre_visitante:20s}: {analisis['porcentaje_victoria_visitante']:6.2f}% ({analisis['victorias_visitante']:,} veces)")
        
        print(f"\n MARCADORES MÁS PROBABLES:")
        for i, (marcador, frecuencia) in enumerate(analisis['marcadores_mas_comunes'], 1):
            probabilidad = (frecuencia / analisis['total_simulaciones']) * 100
            print(f"   {i}. {marcador[0]}-{marcador[1]:1d} → {probabilidad:5.2f}% ({frecuencia:,} veces)")
        
        # Determinar el resultado más probable
        print(f"\n{'='*60}")
        print(f"PRONÓSTICO FINAL")
        print(f"{'='*60}")
        
        max_porcentaje = max(
            analisis['porcentaje_victoria_local'],
            analisis['porcentaje_empate'],
            analisis['porcentaje_victoria_visitante']
        )
        
        if max_porcentaje == analisis['porcentaje_victoria_local']:
            pronostico = f"Victoria de {self.nombre_local}"
        elif max_porcentaje == analisis['porcentaje_victoria_visitante']:
            pronostico = f"Victoria de {self.nombre_visitante}"
        else:
            pronostico = "Empate"
        
        marcador_mas_probable = analisis['marcadores_mas_comunes'][0][0]
        
        print(f"Resultado más probable: {pronostico}")
        print(f"Marcador más probable: {marcador_mas_probable[0]}-{marcador_mas_probable[1]}")
        print(f"{'='*60}\n")


def main():
    print("\n" + "="*60)
    print("  SIMULADOR DE PREDICCIÓN DE PARTIDOS DE FÚTBOL")
    print("  Simulación Monte Carlo con Distribución de Poisson")
    print("="*60)
    
    # Solicitar datos del equipo local
    print("\n--- EQUIPO LOCAL ---")
    nombre_local = input("Nombre del equipo local: ").strip() or "Equipo Local"
    
    print(f"\nEstadísticas de {nombre_local}:")
    posesion_local = float(input("  Posesión promedio (%): ") or "55")
    tiros_local = float(input("  Tiros al arco por partido: ") or "12")
    efectividad_local = float(input("  Efectividad en goles (%): ") or "15")
    
    # Solicitar datos del equipo visitante
    print("\n--- EQUIPO VISITANTE ---")
    nombre_visitante = input("Nombre del equipo visitante: ").strip() or "Equipo Visitante"
    
    print(f"\nEstadísticas de {nombre_visitante}:")
    posesion_visitante = float(input("  Posesión promedio (%): ") or "45")
    tiros_visitante = float(input("  Tiros al arco por partido: ") or "10")
    efectividad_visitante = float(input("  Efectividad en goles (%): ") or "12")
    
    # Número de simulaciones
    print("\n--- PARÁMETROS DE SIMULACIÓN ---")
    num_simulaciones = int(input("Número de simulaciones Monte Carlo (default 100): ") or "100")
    
    # Crear simulador
    simulador = SimuladorPartido(nombre_local, nombre_visitante)
    
    # Calcular goles esperados
    goles_esperados_local = simulador.calcular_goles_esperados(
        posesion_local, tiros_local, efectividad_local
    )
    goles_esperados_visitante = simulador.calcular_goles_esperados(
        posesion_visitante, tiros_visitante, efectividad_visitante
    )
    
    # Ejecutar simulación Monte Carlo
    resultados, marcadores = simulador.simulacion_monte_carlo(
        goles_esperados_local, goles_esperados_visitante, num_simulaciones
    )
    
    # Analizar resultados
    analisis = simulador.analizar_resultados(resultados, marcadores)
    
    # Mostrar resultados
    simulador.mostrar_resultados(analisis, goles_esperados_local, goles_esperados_visitante)


if __name__ == "__main__":
    # Configurar semilla aleatoria para reproducibilidad (opcional)
    # np.random.seed(42)
    # random.seed(42)
    
    main()