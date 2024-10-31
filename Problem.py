# Mathieu Philippot et Adrien Wils

import random
from typing import List
from Pieces import Piece 
from Evaluation import Evaluation
import math

from Heuristiques import Swap_region_mutation, SwapAndRotateInner,SwapBorders,SwapInner,ThreeSwapInner, RotateInner

class Problem:

    @staticmethod
    def load_puzzle(file_path: str) -> tuple[int, int, List[Piece]]:
        """
        Args:
        - file_path (str): Le chemin vers le fichier contenant les informations du puzzle.

        Returns:
        - tuple[int, int, list[Piece]]: Un tuple contenant la largeur du puzzle, la hauteur du puzzle, 
        et une liste de pièces où chaque pièce est représentée par une instance de la classe Piece.
        """
         
        with open(file_path, 'r') as f:
            lines = f.readlines()
        
        # Lecture de la hauteur et de la largeur en utilisant l'espace comme repère (et conversion en int)
        l, h = map(int, lines[0].split())
        pieces = [Piece(*map(int, line.split())) for line in lines[1:]]  # Le reste ce sont les pièces
        
        return l, h, pieces


    @staticmethod
    def initialize_solution(l, h, pieces) -> list:
        """
        Initialise une solution pour le puzzle en plaçant les coins, les bords et les pièces internes de manière aléatoire, tout en respectant les contraintes

        Args:
        - l (int): La largeur du puzzle.
        - h (int): La hauteur du puzzle.
        - pieces (list): Une liste de pièces

        Returns:
        - list: Une liste représentant la solution du puzzle où chaque élément est un tuple (idx, rotation).
            - idx est l'indice de la pièce dans la liste des pièces, et rotation est un entier de 0 à 3
            - indiquant la rotation de la pièce (0: rotation de 0 degré, 1: rotation de 90 degrés, etc.).
        """
        corner_positions = [0, l-1, (l*h)-h, (l*h)-1]
        
        top_edge_positions = [i for i in range(1, l-1)]
        bottom_edge_positions = [i for i in range(l*(h-1)+1, l*h-1)]
        left_edge_positions = [i*l for i in range(1, h-1)]
        right_edge_positions = [i*l+l-1 for i in range(1, h-1)]
        
        edge_positions = top_edge_positions + bottom_edge_positions + left_edge_positions + right_edge_positions
        
        corner_pieces = [idx for idx, piece in enumerate(pieces) if piece.is_corner_piece()]
        edge_pieces = [idx for idx, piece in enumerate(pieces) if piece.is_edge_piece()]
        inner_pieces = [idx for idx, piece in enumerate(pieces) if idx not in corner_pieces + edge_pieces]

        random.shuffle(corner_pieces)
        random.shuffle(edge_pieces)
        random.shuffle(inner_pieces)
        
        # Initialisation de la solution avec une liste "nulle"
        solution = [-1] * (l * h)  
        
        # Coins
        for position in corner_positions:
            idx = corner_pieces.pop()
            if position == 0:
                solution[position] = (idx, 1)
            elif position == l-1:
                solution[position] = (idx, 2)
            elif position == (l*h)-h:
                solution[position] = (idx, 0)
            elif position == (l*h)-1:
                solution[position] = (idx, 3)
                
        # Bordures
        for position in edge_positions:
            idx = edge_pieces.pop()
            if position < l: #dessus
                solution[position] = (idx, 2)
            elif position % l == 0: #gauche
                solution[position] = (idx, 1)
            elif (position + 1) % l == 0: #droite
                solution[position] = (idx, 3)
            else:
                solution[position] = (idx, 0)

        # Pièces internes
        for i in range(l*h):
            if solution[i] == -1:  
                idx = inner_pieces.pop()
                rotation = random.randint(0, 3)
                solution[i] = (idx, rotation)

        return solution

    @staticmethod
    def tournament_selection(population: list, fitness_scores: list, tournament_size: int) -> list:
        """
        Sélectionne aléatoirement une partie des parents, puis sélectionne les meilleurs parmi eux en utilisant un tournoi.

        Args:
        - population (list):
        - fitness_scores (list): Une liste des scores de fitness correspondant à chaque individu dans la population.
        - tournament_size (int): La taille du tournoi ie le nb d'individus sélectionnés pour chaque tournoi. On prendra 3 par défaut.

        Returns:
        - list: Une liste des meilleurs individus sélectionnés
        """

        selected_parents = []
        population_size = len(population)
        for _ in range(population_size):
            contenders_idx = random.sample(range(population_size), tournament_size)
            best_idx = max(contenders_idx, key=lambda idx: fitness_scores[idx])
            selected_parents.append(population[best_idx])

        return selected_parents

    @staticmethod
    def multi_point_crossover(parents, l, h, pieces, num_points=4):
        """
        Effectue le croisement entre les parents pour générer des enfants, en conservant les bords et coins des parents. 

        Returns:
        - list: Une liste des enfants générés par croisement.
        """
        children = []
        population_size = len(parents)
        board_size = l * h
        
        for _ in range(0, population_size, 2):
            parent1, parent2 = random.sample(parents, 2)
            child1, child2 = [(-1, -1)] * board_size, [(-1, -1)] * board_size
            
            # Générer des points de coupure uniques et triés
            cut_points = sorted(random.sample(range(1, board_size), num_points))
            
            # Ajouter les points de début et de fin pour faciliter la boucle
            cut_points = [0] + cut_points + [board_size]
            
            # Alterner entre les parents pour les segments
            source_parent = parent1
            for i in range(len(cut_points)-1):
                start, end = cut_points[i], cut_points[i+1]
                child1[start:end] = source_parent[start:end]
                child2[start:end] = (parent1 if source_parent is parent2 else parent2)[start:end]
                source_parent = parent1 if source_parent is parent2 else parent2
            
            # Réparer les enfants s'il y a des doublons ou des pièces manquantes
            child1 = Problem.repair_child(child1, pieces)
            child2 = Problem.repair_child(child2, pieces)
            
            children.extend([child1, child2])
        
        return children

    @staticmethod
    def repair_child(child, pieces):
        used_pieces = set()
        for idx, rotation in child:
            if idx != -1:
                used_pieces.add(idx)
        
        # Trouver les pièces manquantes en utilisant les indices de `pieces`
        missing_pieces = set(range(len(pieces))) - used_pieces
        
        # Remplacer les doublons par des pièces manquantes
        new_child = []
        seen = set()
        for idx, rotation in child:
            if idx in seen or idx == -1:
                new_idx = missing_pieces.pop()  # Prendre une pièce manquante
                new_child.append((new_idx, random.randint(0, 3)))  # Ajouter avec une rotation aléatoire
            else:
                seen.add(idx)
                new_child.append((idx, rotation))
        
        return new_child

    @staticmethod
    def mutation_adjusted(individual: list, mutation_rate: float, l: int, h: int, corner_positions: list, edge_positions: list, generation: int) -> list: 
        """
        Effectue la mutation des pièces à l'aide de différentes heuristiques, en fonction de l'avancée dans la run.
    
        """       
        # On va d'abord s'occuper des bords car c'est important d'avoir une bonne base et c'est du score facile
        if generation < 200 : 
            return SwapBorders(individual, edge_positions)
        mutation_func = None
        # On essaie d'améliorer les matchs avec des swap et rotations
        if generation < 500:
            mutation_func = random.choice([SwapInner, RotateInner, SwapAndRotateInner, ThreeSwapInner])
        # On va chercher des différences plus marqués pour diversifier et éviter de stagner
        elif generation < 5001:
            region_size = random.randint(4, 15)
            region_start = random.randint(0, len(individual) - region_size)
            mutation_func = Swap_region_mutation
            return mutation_func(individual, mutation_rate, region_size, region_start)
        return mutation_func(individual, mutation_rate, l, h, corner_positions, edge_positions)
        
    @staticmethod
    def mutate_solution(solution, l, h, pieces, corner_positions: list, edge_positions: list, generation:int, mutation_rate:int):
        """
        Fonction de mutation utilisée UNIQUEMENT pour le recuit simulé.
        """
        new_solution = solution.copy() 
        if generation <1400 : 
            piece_to_mutate = random.randint(0, len(solution) - 1)  
            current_rotation = solution[piece_to_mutate][1]
            new_rotation = (current_rotation + random.randint(1, 3)) % 4 
            new_solution[piece_to_mutate] = (solution[piece_to_mutate][0], new_rotation)
            

            #mutation_func = random.choice([SwapInner, RotateInner, SwapAndRotateInner, ThreeSwapInner])
            #return(mutation_func(new_solution,mutation_rate=mutation_rate,l=l,h=h,corner_positions= corner_positions, edge_positions=edge_positions ))

        #Pas efficace d'utiliser les autres heuristiques plus poussées pour le recuit
        #elif generation < 1500 : 
         #   region_size = random.randint(4, 10)
          #  region_start = random.randint(0, len(new_solution) - region_size)
           # return Swap_region_mutation(new_solution, mutation_rate=mutation_rate, region_size=region_size, region_start=region_start)
        
        return new_solution
    
    @staticmethod
    def simulated_annealing(solution, fitness, current_temperature, l, h, pieces, corner_positions: list, edge_positions: list, generation:int, mutation_rate:int):
        """Recuit simulé. On effectue une copie de notre solution puis, on va venir muter la solution et éventuellement l'accepter."""
        new_solution = Problem.mutate_solution(solution, l, h, pieces, corner_positions, edge_positions, generation, mutation_rate)  
        delta_fitness = Evaluation.evaluate_solution(l, h, pieces, new_solution) - fitness
        if delta_fitness > 0 or math.exp(delta_fitness / current_temperature) > random.random():
            return new_solution  
        return solution


    @staticmethod
    def genetic_algorithm(l: int, h: int, pieces: list, population_size: int, generations: int, mutation_rate: float, temperature: int, cooling_rate: int, tournament_size:int) -> tuple[list, int]:
        """
        Implémente l'algorithme génétique en utilisant les fonctions définis au dessus.

        Args:
        - l (int), h (int): La largeur et hauteur du puzzle.
        - pieces (list): Une liste de pièces, chaque pièce étant une liste de quatre entiers représentant les bords.
        - population_size (int): La taille de la population d'individus. 
        - generations (int): Le nombre de générations pour lesquelles l'algorithme génétique est exécuté. 
        - mutation_rate (float): Taux de mutation influençant la quantité d'individus modifiés
        - Temperature et colling_rate : Hyper paramètres utiles à l'acceptation des solutions pour éviter des maximums locaux

        Returns:
        - tuple: Un tuple contenant la meilleure solution trouvée (list) et son score de fitness (int).
        """

        corner_positions = [0, l-1, (l*h)-h, (l*h)-1]
        top_edge_positions = [i for i in range(1, l-1)]
        bottom_edge_positions = [i for i in range(l*(h-1)+1, l*h-1)]
        left_edge_positions = [i*l for i in range(1, h-1)] #On ne prend pas les corners 
        right_edge_positions = [i*l+l-1 for i in range(1, h-1)] # C'est la gauche + (l-1)
        edge_positions = top_edge_positions + bottom_edge_positions + left_edge_positions + right_edge_positions # Ensemble des bords

        population = [Problem.initialize_solution(l, h, pieces) for _ in range(population_size)]
        best_fitness = -1
        best_solution = None
        stagnation_counter = 0
        increased_mutation = False
        original_mutation_rate = mutation_rate
        

        for generation in range(generations):
            fitness_scores = [Evaluation.evaluate_solution(l, h, pieces, solution) for solution in population]

            for i, fitness in enumerate(fitness_scores):
                if fitness > best_fitness:
                    best_fitness = fitness
                    best_solution = population[i]
                    stagnation_counter = 0
                    if increased_mutation:
                        mutation_rate = original_mutation_rate
                        increased_mutation = False
                else:
                    stagnation_counter += 1  

                if stagnation_counter >= 20 and not increased_mutation:
                    mutation_rate *= 5
                    increased_mutation = True
                    stagnation_counter = 0  
                    
                mutation_rate = min(mutation_rate, 0.5)  
    
            """AFFICHAGE POUR LE PLAISIR OU DEBUG"""
            print(f"Génération {generation + 1}: Meilleure fitness = {best_fitness}")

            parents = Problem.tournament_selection(population, fitness_scores, tournament_size)
            children = Problem.multi_point_crossover(parents, l, h, pieces)
            mutated_children = [Problem.mutation_adjusted(child, mutation_rate, l, h, corner_positions, edge_positions, generation) for child in children]
            
            for i in range(0, len(mutated_children), 3): 
                fitness_before = Evaluation.evaluate_solution(l, h, pieces, mutated_children[i])
                mutated_children[i] = Problem.simulated_annealing(mutated_children[i], fitness_before, temperature, l, h, pieces, corner_positions, edge_positions, generation, mutation_rate)
    
            # On refroidit la température 
            temperature *= cooling_rate
            population = mutated_children

        print(f"Meilleure fitness atteinte : {best_fitness}")
        return best_solution, best_fitness
