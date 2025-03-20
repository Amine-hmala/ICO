from mesa import Agent, Model
from mesa.time import RandomActivation
import numpy as np
from genetic_algorithm import genetic_algorithm
from tabu_search import tabu_search, calculate_cost, plot_solution
from simulated_annealing import simulated_annealing
from client_generator import random_clients_generator

# Génération des clients et de la matrice de distances en dehors du modèle
NUM_CUSTOMERS = 12
NUM_VEHICLES = 4
distance_matrix, locations = random_clients_generator(NUM_CUSTOMERS - 1)

class OptimizationAgent(Agent):
    def __init__(self, unique_id, model, algorithm):
        super().__init__(unique_id, model)
        self.algorithm = algorithm
        self.best_solution = None
        self.best_cost = float('inf')

    def step(self):
        customers = self.model.customers
        
        if self.algorithm == 'genetic':
            solution, cost = genetic_algorithm(customers, distance_matrix, NUM_VEHICLES, locations)
        elif self.algorithm == 'tabu':
            solution, cost = tabu_search(customers, distance_matrix, NUM_VEHICLES, locations)
        elif self.algorithm == 'annealing':
            solution, cost = simulated_annealing(customers, distance_matrix, NUM_VEHICLES, locations)
        
        if cost < self.best_cost:
            self.best_solution = solution
            self.best_cost = cost
            
        # Partage des solutions avec les autres agents
        self.model.share_solution(self.best_solution, self.best_cost)

class OptimizationModel(Model):
    def __init__(self, num_agents=3):
        self.schedule = RandomActivation(self)
        self.num_agents = num_agents
        self.customers = list(range(1, NUM_CUSTOMERS))
        self.best_global_solution = None
        self.best_global_cost = float('inf')
        
        algorithms = ['genetic', 'tabu', 'annealing']
        for i in range(num_agents):
            agent = OptimizationAgent(i, self, algorithms[i])
            self.schedule.add(agent)
    
    def share_solution(self, solution, cost):
        if cost < self.best_global_cost:
            self.best_global_solution = solution
            self.best_global_cost = cost
    
    def step(self):
        self.schedule.step()
        print(f"Meilleure solution globale : {self.best_global_solution}, Coût : {self.best_global_cost}")

if __name__ == "__main__":
    model = OptimizationModel()
    for i in range(10):  # Nombre d'itérations de la simulation
        model.step()
    print("Solution finale optimisée :", model.best_global_solution)
    print("Coût final optimisé :", model.best_global_cost)
    
    # Affichage de la meilleure solution obtenue
    if model.best_global_solution:
        plot_solution(model.best_global_solution, locations)
