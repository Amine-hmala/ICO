import numpy as np
import random
import copy
import matplotlib.pyplot as plt
from neighbour import Voisinage_simple
from client_generator import random_clients_generator
from tabu_search import calculate_cost, plot_solution

# Algorithme génétique amélioré inspiré du TD3

def croisementOr(parent1, parent2):
    """Crossover entre deux parents en sélectionnant un segment du premier parent et en complétant avec le second."""
    childP1 = []
    childP2 = []

    geneA = random.randint(0, len(parent1))
    geneB = random.randint(0, len(parent1))
    startGene = min(geneA, geneB)
    endGene = max(geneA, geneB)

    for i in range(startGene, endGene):
        childP1.append(parent1[i])
    
    childP2 = [item for item in parent2 if item not in childP1]
    return childP1 + childP2

def mutation(individual, mutationRate):
    """Mutation en échangeant deux clients aléatoires."""
    for swapped in range(len(individual)):
        if random.random() < mutationRate:
            swapWith = random.randint(0, len(individual)-1)
            individual[swapped], individual[swapWith] = individual[swapWith], individual[swapped]
    return individual

def genetic_algorithm(customers, distance_matrix, num_vehicles, locations, population_size=20, generations=100, mutation_rate=0.1, elite_size=2):
    """
    Implémente l'algorithme génétique pour optimiser la solution du VRP.
    """
    def nouvelleGeneration(pool, eliteSize):
        """Génère la nouvelle population en croisant et mutant les parents sélectionnés."""
        children = []
        length = len(pool) - eliteSize
        pool = random.sample(pool, len(pool))  # Mélange la population

        for i in range(0, eliteSize):
            children.append(pool[i])  # Conserve les meilleurs individus

        for i in range(0, length):
            child = croisementOr(pool[i], pool[len(pool)-i-1])
            children.append(child)
        return children

    # Initialisation de la population
    population = [[list(route) for route in np.array_split(customers, num_vehicles)] for _ in range(population_size)]
    
    for _ in range(generations):
        # Tri de la population en fonction du coût
        population = sorted(population, key=lambda sol: calculate_cost(sol, distance_matrix))
        new_population = nouvelleGeneration(population[:population_size//2], elite_size)
        population = [mutation(ind, mutation_rate) for ind in new_population]
    
    # Sélection de la meilleure solution trouvée
    best_solution = min(population, key=lambda sol: calculate_cost(sol, distance_matrix))
    best_cost = calculate_cost(best_solution, distance_matrix)
    
 
    return best_solution, best_cost

# Test de l'algorithme génétique
if __name__ == "__main__":
    number = 12
    customers = list(range(1, number))
    depot = 0
    num_vehicles = 4
    Clients = random_clients_generator(number - 1)
    distance_matrix = Clients[0]
    locations = Clients[1]
    
    print("Exécution de l'algorithme génétique...")
    ga_routes, ga_cost = genetic_algorithm(customers, distance_matrix, num_vehicles, locations)
    print("Meilleures routes trouvées:", ga_routes)
    print("Coût optimal trouvé:", ga_cost)
