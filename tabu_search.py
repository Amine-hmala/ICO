import numpy as np
import Voisinage
import copy
import matplotlib.pyplot as plt
import random

def calculate_cost(routes, distance_matrix, w=2):
    """Calculates the total cost of a solution by summing up the distances for each route."""
    total_cost = 0
    
    for route in routes:
        if not route:
            continue  # Skip empty routes
        route = [0] + route + [0]  # Ensure each route starts and ends at the depot
        route_cost = sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1))
        total_cost += route_cost
    
    total_cost += w * len(routes)  # Penalty for number of vehicles
    return total_cost

def generate_initial_solution(customers, num_vehicles):
    """Generates an initial solution by randomly distributing customers among vehicles."""
    random.shuffle(customers)
    routes = np.array_split(customers, num_vehicles)
    return [list(route) for route in routes]

def tabu_search(customers, distance_matrix, max_iterations=100, tabu_tenure=10, num_vehicles=3):
    best_solution = generate_initial_solution(customers, num_vehicles)
    best_cost = calculate_cost(best_solution, distance_matrix)
    current_solution = copy.deepcopy(best_solution)
    current_cost = best_cost
    tabu_list = []
    
    for _ in range(max_iterations):
        neighborhood = Voisinage.Voisinage_list(current_solution)  # Generate neighbors
        best_neighbor = None
        best_neighbor_cost = float('inf')
        
        for neighbor in neighborhood:
            if neighbor not in tabu_list:
                neighbor_cost = calculate_cost(neighbor, distance_matrix)
                if neighbor_cost < best_neighbor_cost:
                    best_neighbor = neighbor
                    best_neighbor_cost = neighbor_cost
        
        if best_neighbor is not None:
            current_solution = copy.deepcopy(best_neighbor)
            current_cost = best_neighbor_cost
            tabu_list.append(copy.deepcopy(best_neighbor))
            
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)
            
            if current_cost < best_cost:
                best_solution = copy.deepcopy(current_solution)
                best_cost = current_cost
    
    return best_solution, best_cost

def plot_solution(routes, locations):
    """Plots the VRP solution using matplotlib."""
    plt.figure(figsize=(8, 6))
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    depot = locations[0]
    plt.scatter(depot[0], depot[1], c='k', marker='s', s=200, label='Depot')

    for i, route in enumerate(routes):
        route = [0] + route + [0]
        x, y = [locations[n][0] for n in route], [locations[n][1] for n in route]
        plt.plot(x, y, color=colors[i % len(colors)], marker='o', label=f'Vehicle {i+1}')

    plt.legend()
    plt.title("VRP Solution")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(False)
    plt.show()
