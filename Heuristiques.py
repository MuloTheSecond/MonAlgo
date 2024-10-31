import random
from Pieces import Piece

def SwapInner(individual: list, mutation_rate: float, l: int, h: int, corner_positions: list, edge_positions: list)-> list:
    """
        Effectue la mutation des pièces en permutant deux pièces choisies aléatoirement, avec une probabilité donnée.

        Args:
        - individual (list): La solution individuelle à muter.
        - mutation_rate (float): Le taux de mutation, indiquant la probabilité qu'une mutation se produise pour chaque pièce interne.
        - l, h, corner_positions, edge_positions : comme avant

        Returns:
        - list: La solution individuelle mutée.
        """
    for i in range(len(individual)):
        if random.random() < mutation_rate:
            if i not in corner_positions + edge_positions:  # On ne bouge que les pièces du centre 
                idx2 = i
                while idx2 in corner_positions + edge_positions or idx2 == i: # Idem, on ne garde pas le nouvel indice s'il est un coin/bord ou si c'est le même
                    idx2 = random.randint(0, len(individual) - 1)
                individual[i], individual[idx2] = individual[idx2], individual[i]
            
    return individual

def SwapBorders(individual: list, edge_positions: list) -> list:
    """
    Effectue le swap de deux pièces sur les bords du puzzle et applique les rotations nécessaires.

    Args:
    - individual (list): La solution individuelle à muter.
    - edge_positions (list): Les positions des bords du puzzle.

    Returns:
    - list: La solution individuelle mutée.
    """
    idx1, idx2 = random.sample(edge_positions, 2)

    piece_idx1, rot1 = individual[idx1]
    #piece1 = pieces[piece_idx1] 
    piece_idx2, rot2 = individual[idx2]
    #piece2 = pieces[piece_idx2] 

    individual[idx1] = (piece_idx2, rot1)
    individual[idx2] = (piece_idx1, rot2)
    
    return individual


def RotateInner(individual: list, mutation_rate: float, l: int, h: int, corner_positions: list, edge_positions: list) -> list:
    """
    Effectue la rotation de deux pièces internes choisies aléatoirement.

    Args:
    - individual (list): La solution individuelle à muter.
    - l, h, corner_positions, edge_positions : paramètres 

    Returns:
    - list: La solution individuelle mutée.
    """
    for _ in range(2):  # On sélectionne deux pièces internes aléatoires
        idx = random.randint(0, len(individual) - 1)
        while idx in corner_positions + edge_positions:  # On vérifie qu'on a sélectionné une pièce interne
            idx = random.randint(0, len(individual) - 1)
        
        # On effectue la rotation d'une unité (faire aussi aléatoire ?)
        piece_idx, rotation = individual[idx]
        individual[idx] = (piece_idx, (rotation + 1) % 4)

    return individual

def SwapAndRotateInner(individual: list, mutation_rate: float, l: int, h: int, corner_positions: list, edge_positions: list) -> list:
    """
    Effectue la permutation et la rotation de deux pièces internes choisies aléatoirement.

    Args:
    - individual (list): La solution individuelle à muter.
    - l, h, corner_positions, edge_positions : paramètres 

    Returns:
    - list: La solution individuelle mutée.
    """
    for _ in range(2):  # On sélectionne deux pièces internes aléatoires
        idx1 = random.randint(0, len(individual) - 1)
        idx2 = random.randint(0, len(individual) - 1)
        while idx1 in corner_positions + edge_positions or idx2 in corner_positions + edge_positions or idx2 == idx1:  
            idx1 = random.randint(0, len(individual) - 1)
            idx2 = random.randint(0, len(individual) - 1)
        
        # Permutation des pièces
        individual[idx1], individual[idx2] = individual[idx2], individual[idx1]

        # Rotation d'une unité pour chaque pièce
        for idx in (idx1, idx2):
            piece_idx, rotation = individual[idx]
            individual[idx] = (piece_idx, (rotation + 1) % 4)

    return individual

def ThreeSwapInner(individual: list, mutation_rate: float, l: int, h: int, corner_positions: list, edge_positions: list) -> list:
    """
    Effectue l'échange et la rotation de trois pièces internes choisies aléatoirement.

    """

    idx1 = random.randint(0, len(individual) - 1)
    idx2 = random.randint(0, len(individual) - 1)
    idx3 = random.randint(0, len(individual) - 1)
    
    while idx1 in corner_positions + edge_positions or idx2 in corner_positions + edge_positions or idx3 in corner_positions + edge_positions or idx2 == idx1 or idx3 == idx1 or idx3 == idx2:  
        idx1 = random.randint(0, len(individual) - 1)
        idx2 = random.randint(0, len(individual) - 1)
        idx3 = random.randint(0, len(individual) - 1)

    individual[idx1], individual[idx2], individual[idx3] = individual[idx2], individual[idx3], individual[idx1]


    return individual

def Swap_region_mutation(individual: list, mutation_rate: float, region_size: int, region_start: int,):
    """
    Effectue la mutation d'échange de région sur l'individu donné.

    Args:
    - individual (list): L'individu à muter.
    - mutation_rate (float): Le taux de mutation.
    - region_start (int): Le début de la région à échanger.
    - region_size (int): La taille de la région à échanger.

    Returns:
    - list: L'individu muté.
    """
    if random.random() < mutation_rate:
        # On prends un autre région de même dimension
        other_region_start = random.randint(0, len(individual) - region_size)

        # Échange des régions
        individual[region_start:region_start+region_size], individual[other_region_start:other_region_start+region_size] = \
            individual[other_region_start:other_region_start+region_size], individual[region_start:region_start+region_size]

    return individual

def Rotate_region_mutation(individual: list, mutation_rate: float, region_start: int, region_size: int):
    """
    Effectue la mutation de rotation sur une région spécifiée de l'individu.
    """
    if random.random() < mutation_rate:
        individual[region_start:region_start+region_size] = individual[region_start+1:region_start+region_size] + [individual[region_start]]

    return individual
