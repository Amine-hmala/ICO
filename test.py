import numpy as np
import random
import matplotlib.pyplot as plt
def Voisinage_simple(routes):
    new_routes = [route[:] for route in routes]  # Copy the current routes
    route1, route2 = random.sample(new_routes, 2)  # Select two different routes # see if it iss possible to not swap every time
    if route1 and route2:  # Ensure both are non-empty
        idx1, idx2 = random.randint(0, len(route1)-1), random.randint(0, len(route2)-1)
        route1[idx1], route2[idx2] = route2[idx2], route1[idx1]  # Swap customers
    
    #NAR
    a = random.randint(1,10)
    b = random.randint(1,12-a-1)
    Stops = [item for sublist in new_routes for item in sublist]
    A = Stops[:a]
    B = Stops[a:b+a]
    C = Stops[b+a :]
    return [A,B,C]
def Voisinage_list(routes,nb_voisinage = 50):
    L=list()
    for i in range(nb_voisinage):
           L += Voisinage_simple(routes)
    return L


def calculate_cost(routes, distance_matrix, w =2):
    """Calculates the total cost of a solution by summing up the distances for each route."""
    total_cost = 0
    
    for route in routes:
        route_cost = distance_matrix[0][route[0]]+ sum(distance_matrix[route[i]][route[i+1]] for i in range(len(route)-1)) + distance_matrix[route[len(route)-1]][0]
        total_cost += route_cost
    total_cost += w*len(routes)
    return total_cost

def generate_initial_solution(customers, num_vehicles):
    """Generates an initial solution by randomly distributing customers among vehicles."""
    random.shuffle(customers)
    routes = np.array_split(customers, num_vehicles)  # Split customers into roughly equal parts
    return [list(route) for route in routes]
'''

def perturb_solution(routes):
    """Applies a small random modification to the solution by swapping customers between routes."""
    new_routes = [route[:] for route in routes]  # Copy the current routes
    route1, route2 = random.sample(new_routes, 2)  # Select two different routes
    if route1 and route2:  # Ensure both are non-empty
        idx1, idx2 = random.randint(0, len(route1)-1), random.randint(0, len(route2)-1)
        route1[idx1], route2[idx2] = route2[idx2], route1[idx1]  # Swap customers
    return new_routes

def simulated_annealing(customers, num_vehicles, distance_matrix, initial_temp=1000, cooling_rate=0.99, min_temp=1):
    """Solves the VRP using Simulated Annealing."""
    # Generate initial random solution
    current_solution = generate_initial_solution(customers, num_vehicles)
    current_cost = calculate_cost(current_solution, distance_matrix)
    best_solution, best_cost = current_solution, current_cost

    temp = initial_temp  # Start with a high temperature

    while temp > min_temp:
        new_solution = perturb_solution(current_solution)  # Generate a new neighbor solution
        new_cost = calculate_cost(new_solution, distance_matrix)

        # Accept new solution if it's better or with a probability based on the temperature
        if new_cost < current_cost or random.random() < np.exp((current_cost - new_cost) / temp):
            current_solution, current_cost = new_solution, new_cost
            if new_cost < best_cost:
                best_solution, best_cost = new_solution, new_cost

        temp *= cooling_rate  # Reduce temperature

    return best_solution, best_cost

def plot_solution(routes, locations):
    """Plots the VRP solution using matplotlib."""
    plt.figure(figsize=(8, 6))
    colors = ['b', 'g', 'r', 'c', 'm', 'y']
    depot = locations[0]
    plt.scatter(depot[0], depot[1], c='k', marker='s', s=200, label='Depot')  # Larger marker for depot

    for i, route in enumerate(routes):
        route = [0] + route + [0]  # Ensure each route starts and ends at the depot
        x, y = [locations[n][0] for n in route], [locations[n][1] for n in route]
        plt.plot(x, y, color=colors[i % len(colors)], marker='o', label=f'Vehicle {i+1}')

    plt.legend()
    plt.title("VRP Solution")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.grid(False)  # Grid removed for a cleaner look
    plt.show()
'''
# Example Usage
# Define parameters for the problem
distance_matrix = np.random.randint(1, 100, size=(13, 13))  # Generate a random distance matrix
np.fill_diagonal(distance_matrix, 0)  # Set diagonal to 0 as a location has no distance to itself

#print(distance_matrix)

customers = list(range(1, 13))  # Customers indexed from 1 to 12
depot = 0  # Depot is at index 0
num_vehicles = 3  # Number of available vehicles
'''

# Generate random locations for visualization
locations = {i: (random.randint(0, 100), random.randint(0, 100)) for i in range(13)}

# Run the Simulated Annealing algorithm
best_routes, best_cost = simulated_annealing(customers, num_vehicles, distance_matrix, initial_temp = 9999999999999, cooling_rate = 0.9999, min_temp = 10)

print("Best Routes:", best_routes)
print("Best Cost:", best_cost)

# Plot the solution
plot_solution(best_routes, locations)
'''

routes = [[i] for i in range(1,13)]
nb_vehicules = len(routes)
flat_list = [item for sublist in routes for item in sublist]
#L = flat_list[3:5]
#print(flat_list)
#print("cceci est la route", routes )
#print(calculate_cost(routes,distance_matrix))import random
import numpy as np

def tabu_search(customers, distance_matrix, max_iterations=100, tabu_tenure=10, num_vehicles = 3):
    best_solution = generate_initial_solution(customers, num_vehicles)
    best_cost = calculate_cost(best_solution, distance_matrix)
    current_solution = best_solution[:]
    current_cost = best_cost
    tabu_list = []
    print(best_cost)
    
    for _ in range(max_iterations):
        neighborhood = Voisinage_list(current_solution)
        print(neighborhood)
        best_neighbor = None
        best_neighbor_cost = float('inf')
        
        for neighbor in neighborhood:
            if neighbor not in tabu_list:
                print(neighbor)
                neighbor_cost = calculate_cost(neighbor, distance_matrix)
                if neighbor_cost < best_neighbor_cost:
                    best_neighbor = neighbor
                    best_neighbor_cost = neighbor_cost
        
        if best_neighbor is not None:
            current_solution = best_neighbor
            current_cost = best_neighbor_cost
            tabu_list.append(best_neighbor)
            
            if len(tabu_list) > tabu_tenure:
                tabu_list.pop(0)
            
            if current_cost < best_cost:
                best_solution = current_solution[:]
                best_cost = current_cost
    
    return best_solution, best_cost
print(tabu_search(customers,distance_matrix = distance_matrix ))