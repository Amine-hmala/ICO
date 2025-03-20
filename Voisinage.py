import random

def Voisinage_simple(routes, num_vehicles):
    new_routes = [route[:] for route in routes]  # Copie des routes actuelles
    if len(new_routes) < num_vehicles:
        return new_routes  # Assurer qu'il y a bien le bon nombre de véhicules
    
    route1, route2 = random.sample(new_routes, 2)  # Sélectionner deux routes différentes
    if route1 and route2:  # S'assurer qu'elles ne sont pas vides
        idx1, idx2 = random.randint(0, len(route1)-1), random.randint(0, len(route2)-1)
        route1[idx1], route2[idx2] = route2[idx2], route1[idx1]  # Échanger des clients
    
    # Générer une solution de voisinage en prenant en compte le nombre de véhicules
    Stops = [item for sublist in new_routes for item in sublist]  # Liste totale des clients
    
    # Assurer une découpe équilibrée avec au moins un client par véhicule
    partitions = sorted(random.sample(range(1, len(Stops)), num_vehicles - 1))
    partitions.append(len(Stops))  # Ajouter la dernière borne
    
    routes_split = []
    prev = 0
    for p in partitions:
        routes_split.append(Stops[prev:p])
        prev = p
    
    return routes_split

def Voisinage_list(routes, num_vehicules , nb_voisinage=50):
    L = []
    for _ in range(nb_voisinage):
        L.append(Voisinage_simple(routes,num_vehicules))  # Append each generated neighbor solution
    return L

#routes = [[i] for i in range(1,13)]
#print(Voisinage_simple(routes))
