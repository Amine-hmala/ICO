import random

def Voisinage_simple(routes):
    new_routes = [route[:] for route in routes]  # Copy the current routes
    if len(new_routes) < 2:
        return new_routes  # No swap possible if less than 2 routes
    
    route1, route2 = random.sample(new_routes, 2)  # Select two different routes
    if route1 and route2:  # Ensure both are non-empty
        idx1, idx2 = random.randint(0, len(route1)-1), random.randint(0, len(route2)-1)
        route1[idx1], route2[idx2] = route2[idx2], route1[idx1]  # Swap customers
    
    # Generate a neighborhood solution
    a = random.randint(1, 10)
    b = random.randint(1, 12 - a - 1)
    Stops = [item for sublist in new_routes for item in sublist]
    A = Stops[:a]
    B = Stops[a:b + a]
    C = Stops[b + a:]
    
    return [A, B, C]

def Voisinage_list(routes, nb_voisinage=50):
    L = []
    for _ in range(nb_voisinage):
        L.append(Voisinage_simple(routes))  # Append each generated neighbor solution
    return L

#routes = [[i] for i in range(1,13)]
#print(Voisinage_simple(routes))
