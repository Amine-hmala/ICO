import tabu_search
import client_generator as gn
import numpy as np
import copy
import matplotlib.pyplot as plt
import random
import simulated_annealing
import genetic_algorithm

'''
# Générer une matrice de distances aléatoires pour 13 emplacements (1 dépôt + 12 clients)
num_locations = 13  # 1 dépôt + 12 clients
distance_matrix = np.random.randint(10, 100, size=(num_locations, num_locations))
np.fill_diagonal(distance_matrix, 0)  # Pas de distance entre un point et lui-même
'''


# Définition du problème
number = 12
customers = list(range(1, number))  # Clients indexés de 1 à 12
depot = 0  # Dépôt est à l'index 0
num_vehicles = 4  # Nombre de véhicules

# Générer la matrice de distances et les positions des clients
Clients = gn.random_clients_generator(number - 1)
distance_matrix = Clients[0]
locations = Clients[1]

# Générer une solution initiale unique
initial_solution = tabu_search.generate_initial_solution(customers, num_vehicles)

# Exécuter la recherche tabou
tabu_routes, tabu_cost = tabu_search.tabu_search(customers, distance_matrix, num_vehicles,locations, max_iterations=100, tabu_tenure=10)
print("Meilleures Routes (Tabou):", tabu_routes)
print("Coût Optimal (Tabou):", tabu_cost)

# Exécuter le recuit simulé
sa_routes, sa_cost = simulated_annealing.simulated_annealing(customers, distance_matrix, num_vehicles, locations, initial_temp=1000, cooling_rate=0.99, max_iterations=500)
print("Meilleures Routes (SA):", sa_routes)
print("Coût Optimal (SA):", sa_cost)

# Exécuter l'algorithme génétique
ga_routes, ga_cost = genetic_algorithm.genetic_algorithm(customers, distance_matrix, num_vehicles, locations, population_size=20, generations=100, mutation_rate=0.1, elite_size=2)
print("Meilleures Routes (GA):", ga_routes)
print("Coût Optimal (GA):", ga_cost)

# Fonction pour afficher les trois solutions côte à côte
def plot_three_solutions(routes1, routes2, routes3, locations, titles):
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))

    colors = ['b', 'g', 'r', 'c', 'm', 'y']

    for idx, (routes, title, ax) in enumerate(zip([routes1, routes2, routes3], titles, axes)):
        ax.set_title(title)
        depot = locations[0]
        ax.scatter(depot[0], depot[1], c='k', marker='s', s=200, label='Dépôt')

        for i, route in enumerate(routes):
            route = [0] + route + [0]
            x, y = [locations[n][0] for n in route], [locations[n][1] for n in route]
            ax.plot(x, y, color=colors[i % len(colors)], marker='o', label=f'Véhicule {i+1}')

        ax.legend()
        ax.set_xlabel("X Coordinate")
        ax.set_ylabel("Y Coordinate")
        ax.grid(False)

    plt.suptitle("Comparaison des solutions des trois algorithmes")
    plt.show()

# Afficher les solutions côte à côte
plot_three_solutions(tabu_routes, sa_routes, ga_routes, locations, ["Tabou", "Recuit Simulé", "Génétique"])
