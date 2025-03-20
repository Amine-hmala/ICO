import tabu_search
import client_generator as gn
import numpy as np
import copy
import matplotlib.pyplot as plt
import random
import simulated_annealing

'''
# Générer une matrice de distances aléatoires pour 13 emplacements (1 dépôt + 12 clients)
num_locations = 13  # 1 dépôt + 12 clients
distance_matrix = np.random.randint(10, 100, size=(num_locations, num_locations))
np.fill_diagonal(distance_matrix, 0)  # Pas de distance entre un point et lui-même
'''
number = 12
# Définir les clients et le dépôt
customers = list(range(1, number))  # Clients indexés de 1 à 12
depot = 0  # Dépôt est à l'index 0
num_vehicles = 4  # Nombre de véhicules

Clients = gn.random_clients_generator(number -1)
distance_matrix = Clients[0]
locations = Clients[1]


# Exécuter la recherche taboue
best_routes_sa, best_cost_sa = simulated_annealing.simulated_annealing(customers, distance_matrix,num_vehicles=num_vehicles,locations= locations, initial_temp=1000, cooling_rate=0.99, max_iterations=500)

# Afficher les résultats
print("Meilleures Routes:", best_routes_sa)
print("Coût Optimal:", best_cost_sa)

tabu_search.plot_solution(best_routes_sa, locations)
