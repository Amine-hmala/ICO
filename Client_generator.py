import numpy as np
import copy
import matplotlib.pyplot as plt
import random

def random_clients_generator(number=12):
        # Générer une matrice de distances aléatoires pour 13 emplacements (1 dépôt + 12 clients)
    num_locations = number + 1  # 1 dépôt + 12 clients
    locations = {i: (random.randint(0, 10), random.randint(0, 10)) for i in range(num_locations)}
    distance_matrix = list()
    for i in range(num_locations):
        distance_matrix.append(list())
        for j in range(num_locations):
            distance_matrix[i].append(np.sqrt((locations[i][0] - locations[j][0])**2 + (locations[i][1] - locations[j][1])**2))
    return(distance_matrix , locations)
#test  random_clients_generator
