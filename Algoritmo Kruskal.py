import time
import matplotlib.pyplot as plt
import networkx as nx

class DisjointSet:
    def __init__(self, ciudades):
        self.parent = {c: c for c in ciudades}
        self.rank = {c: 0 for c in ciudades}

    def find(self, item):
        if self.parent[item] == item:
            return item
        self.parent[item] = self.find(self.parent[item])
        return self.parent[item]

    def union(self, set1, set2):
        root1 = self.find(set1)
        root2 = self.find(set2)
        if root1 != root2:
            if self.rank[root1] > self.rank[root2]:
                self.parent[root2] = root1
            elif self.rank[root1] < self.rank[root2]:
                self.parent[root1] = root2
            else:
                self.parent[root2] = root1
                self.rank[root1] += 1
            return True
        return False

def dibujar_mapa(G, pos, carreteras_aprobadas, carretera_actual=None, titulo=""):
    plt.clf()
    plt.title(titulo, fontsize=12, fontweight='bold')
    
    # Dibujar las ciudades
    nx.draw_networkx_nodes(G, pos, node_color='orange', node_size=700)
    nx.draw_networkx_labels(G, pos, font_weight='bold', font_size=10)
    
    # Dibujar todas las carreteras posibles en gris claro
    nx.draw_networkx_edges(G, pos, edge_color='gainsboro', width=2)
    
    # Dibujar las carreteras ya aprobadas en verde
    if carreteras_aprobadas:
        nx.draw_networkx_edges(G, pos, edgelist=carreteras_aprobadas, edge_color='forestgreen', width=5)
        
    # Dibujar la carretera que se está evaluando en rojo
    if carretera_actual:
        nx.draw_networkx_edges(G, pos, edgelist=[carretera_actual], edge_color='crimson', width=6, style='dashed')
        
    # Dibujar las distancias (kilómetros)
    labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, font_size=10)
    
    plt.pause(2.0) # Pausa de 2 segundos para ver el mapa

def simulador_kruskal_ciudades(lista_ciudades, mapa_carreteras, modo="MIN"):
    print(f"SIMULADOR DE PLANIFICACIÓN DE CARRETERAS ")
    print(f"Objetivo: Conectar todas las ciudades gastando el {'MÍNIMO' if modo == 'MIN' else 'MÁXIMO'} de kilómetros.\n")
    
    # Crear el mapa visual
    G = nx.Graph()
    for origen, destino, kilometros in mapa_carreteras:
        G.add_edge(origen, destino, weight=kilometros)
    
    pos = nx.spring_layout(G, seed=42) 
    plt.figure(figsize=(9, 7))
    plt.ion()
    
    # Ordenar las carreteras por su distancia
    reversa = True if modo == "MAX" else False
    carreteras_ordenadas = sorted(mapa_carreteras, key=lambda x: x[2], reverse=reversa)
    
    print("Carreteras disponibles ordenadas por distancia:")
    for orig, dest, km in carreteras_ordenadas:
        print(f"  * {orig} hacia {dest} -> {km} km")
    print("-" * 60)

    dsu = DisjointSet(lista_ciudades)
    rutas_finales = []
    kilometros_totales = 0
    
    dibujar_mapa(G, pos, rutas_finales, titulo="Mapa Inicial: Todas las ciudades desconectadas")
    time.sleep(1)

    # Evaluar carretera por carretera
    for origen, destino, kilometros in carreteras_ordenadas:
        print(f"Analizando ruta: {origen} - {destino} ({kilometros} km)")
        
        # Mostrar en el mapa la carretera que estamos revisando
        dibujar_mapa(G, pos, rutas_finales, carretera_actual=(origen, destino), 
                     titulo=f"¿Conectamos {origen} con {destino}? ({kilometros} km)")
        
        # Revisar si las ciudades ya están conectadas por otro camino
        if dsu.find(origen) != dsu.find(destino):
            dsu.union(origen, destino)
            rutas_finales.append((origen, destino))
            kilometros_totales += kilometros
            print(f"  => ¡APROBADA! Esta carretera es necesaria. Total acumulado: {kilometros_totales} km")
        else:
            print(f"  => RECHAZADA. ¡No hace falta! Esas ciudades ya tienen una conexión (evitamos un circuito cerrado).")
            
        dibujar_mapa(G, pos, rutas_finales, titulo=f"Carreteras construidas. Total: {kilometros_totales} km")
        print("-" * 60)
        
        # Si ya conectamos todas las ciudades, paramos
        if len(rutas_finales) == len(lista_ciudades) - 1:
            print("¡Perfecto! Todas las ciudades ya están comunicadas entre sí.")
            break

    print("\n=== PLAN DE CONSTRUCCIÓN FINAL ===")
    print(f"Carreteras a construir: {rutas_finales}")
    print(f"Total de asfalto utilizado: {kilometros_totales} km")
    
    plt.ioff()
    dibujar_mapa(G, pos, rutas_finales, titulo=f"Plano Final - Total: {kilometros_totales} km")
    plt.show()


# DATOS DEL MAPA
# 1. Nuestras ciudades
mis_ciudades = ['Madrid', 'Barcelona', 'Valencia', 'Sevilla', 'Bilbao', 'Zaragoza']

# 2. Las carreteras posibles: (Ciudad_A, Ciudad_B, Kilómetros)
mis_carreteras = [
    ('Madrid', 'Barcelona', 600),
    ('Madrid', 'Valencia', 350),
    ('Barcelona', 'Valencia', 350),
    ('Barcelona', 'Zaragoza', 300),
    ('Valencia', 'Sevilla', 650),
    ('Valencia', 'Zaragoza', 400),
    ('Sevilla', 'Bilbao', 900),
    ('Sevilla', 'Zaragoza', 850),
    ('Bilbao', 'Zaragoza', 320)
]

# Se ejecuta el simulador en modo MÍNIMO costo
simulador_kruskal_ciudades(mis_ciudades, mis_carreteras, modo="MIN")