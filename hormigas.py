import numpy as np
import math
import random
import matplotlib.pyplot as plt


coords = [(0,0), (1,5), (4,2), (6,6), (8,3), (3,7), (7,1)]
n = len(coords)

# Distancias euclidianas
dist = np.zeros((n, n))
for i in range(n):
    for j in range(n):
        (x1,y1) = coords[i]
        (x2,y2) = coords[j]
        dist[i][j] = math.hypot(x1-x2, y1-y2)


num_hormigas = 20
num_iter = 200
alpha = 1.0
beta = 5.0
rho = 0.5
Q = 100

pheromone = np.ones((n, n))



def elegir_siguiente(actual, visitado):
    probs = []
    for j in range(n):
        if j in visitado:
            probs.append(0)
        else:
            tau = pheromone[actual][j] ** alpha
            eta = (1.0 / dist[actual][j]) ** beta
            probs.append(tau * eta)

    s = sum(probs)
    if s == 0:
        opciones = [j for j in range(n) if j not in visitado]
        return random.choice(opciones)

    probs = [p/s for p in probs]
    return np.random.choice(range(n), p=probs)


def construir_ruta():
    ruta = [0]
    visitado = set(ruta)

    while len(ruta) < n:
        actual = ruta[-1]
        nxt = elegir_siguiente(actual, visitado)
        ruta.append(nxt)
        visitado.add(nxt)

    ruta.append(0)
    return ruta


def longitud_ruta(ruta):
    return sum(dist[ruta[i]][ruta[i+1]] for i in range(len(ruta)-1))



mejor_ruta = None
mejor_distancia = float("inf")

for it in range(num_iter):

    rutas = []
    distancias = []

    for _ in range(num_hormigas):
        r = construir_ruta()
        d = longitud_ruta(r)

        rutas.append(r)
        distancias.append(d)

        if d < mejor_distancia:
            mejor_distancia = d
            mejor_ruta = r

    pheromone *= (1 - rho)

    for ruta, d in zip(rutas, distancias):
        deposito = Q / d
        for i in range(len(ruta)-1):
            a, b = ruta[i], ruta[i+1]
            pheromone[a][b] += deposito
            pheromone[b][a] += deposito

    if (it + 1) % 20 == 0:
        print(f"Iteración {it+1} → mejor distancia: {mejor_distancia:.3f}")



xs = [coords[i][0] for i in mejor_ruta]
ys = [coords[i][1] for i in mejor_ruta]

plt.figure(figsize=(7,7))
plt.plot(xs, ys, marker='o', linewidth=2)

# Etiquetas de nodos
for i, (x, y) in enumerate(coords):
    plt.text(x + 0.1, y + 0.1, str(i), fontsize=12)

plt.title("Mejor ruta encontrada por ACO")
plt.xlabel("X")
plt.ylabel("Y")
plt.grid(True)
plt.show()

print("\nMejor ruta:", mejor_ruta)
print("Distancia total:", mejor_distancia)
