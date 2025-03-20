import numpy as np
import random
import copy
import matplotlib.pyplot as plt
from neighbour import Voisinage_simple
from client_generator import random_clients_generator
from tabu_search import calculate_cost, plot_solution
import tabu_search


# Algorithme du recuit simulé (Simulated Annealing)
def simulated_annealing(customers, distance_matrix, num_vehicles, locations, initial_temp=1000, cooling_rate=0.99, max_iterations=500):
    """
    Implémente l'algorithme du recuit simulé pour optimiser la solution du VRP.
    
    Paramètres:
    - customers : Liste des clients à desservir
    - distance_matrix : Matrice des distances entre les clients et le dépôt
    - num_vehicles : Nombre de véhicules disponibles
    - locations : Coordonnées des clients et du dépôt
    - initial_temp : Température initiale pour l'algorithme
    - cooling_rate : Taux de refroidissement
    - max_iterations : Nombre maximal d'itérations
    
    Retourne:
    - best_solution : Meilleure solution trouvée
    - best_cost : Coût de la meilleure solution
    """
    best_solution = tabu_search.generate_initial_solution(customers, num_vehicles)
    best_cost = tabu_search.calculate_cost(best_solution, distance_matrix)
    current_solution = copy.deepcopy(best_solution)
    current_cost = best_cost
    temp = initial_temp
    
    for _ in range(max_iterations):
        new_solution = Voisinage_simple(current_solution, num_vehicles)
        new_cost = calculate_cost(new_solution, distance_matrix)
        
        # Accepter une solution pire avec une certaine probabilité
        if new_cost < current_cost or random.uniform(0, 1) < np.exp((current_cost - new_cost) / temp):
            current_solution = copy.deepcopy(new_solution)
            current_cost = new_cost
            
            # Mise à jour de la meilleure solution trouvée
            if current_cost < best_cost:
                best_solution = copy.deepcopy(current_solution)
                best_cost = current_cost
        
        # Refroidissement de la température
        temp *= cooling_rate
    
    
    return best_solution, best_cost
