""" AFFICHAGE """    
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as patches

# ChatGPT : 

def draw_piece(ax, piece, position, size=1):

    colors = {
        0: 'white', 1: 'lightblue', 2: 'lightgreen', 3: 'salmon', 4: 'violet', 
        5: 'red', 6: 'orange', 7: 'grey', 8: 'green', 9: 'pink', 10: 'yellow', 
        11: 'brown', 12: 'turquoise', 13: 'tan', 14: 'skyblue', 15: 'purple', 
        16: 'olive', 17: 'orange', 18: 'lime', 19: 'lavender', 20: 'magenta', 
        21: 'maroon', 22: 'navy', 23: 'aquamarine', 24: 'coral', 25: 'crimson', 
        26: 'khaki', 27: 'gold', 28: 'indigo', 29: 'ivory', 30: 'mintcream'
    }   
    bottom_left = (position[0], position[1])
    bottom_right = (position[0] + size, position[1])
    top_left = (position[0], position[1] + size)
    top_right = (position[0] + size, position[1] + size)
    center = (position[0] + size/2, position[1] + size/2)

    # Define the triangles for each side of the piece
    triangles = {
        'bottom': [bottom_left, bottom_right, center],
        'left': [bottom_left, top_left, center],
        'top': [top_left, top_right, center],
        'right': [bottom_right, top_right, center]
    }

    # Draw each triangle
    for side, points in triangles.items():
        value = piece[['bottom', 'left', 'top', 'right'].index(side)]
        triangle = patches.Polygon(points, closed=True, facecolor=colors[value], edgecolor='black')
        ax.add_patch(triangle)

        # Add text
        if side == 'bottom':
            ax.text(center[0], position[1] + size/4, str(value), ha='center', va='center', fontsize=10)
        elif side == 'left':
            ax.text(position[0] + size/4, center[1], str(value), ha='center', va='center', fontsize=10, rotation=90)
        elif side == 'top':
            ax.text(center[0], position[1] + 3*size/4, str(value), ha='center', va='center', fontsize=10)
        elif side == 'right':
            ax.text(position[0] + 3*size/4, center[1], str(value), ha='center', va='center', fontsize=10, rotation=90)

def draw_full_puzzle(pieces, solution, l, h):
    # Define the figure and axes
    fig, ax = plt.subplots(figsize=(l, h))
    ax.set_xlim(0, l)
    ax.set_ylim(0, h)
    ax.axis('off')  # Turn off the axis
    
    # Color map for the piece edges
    color_map = {0: 'white', 1: 'lightblue', 2: 'lightgreen', 3: 'lightcoral', 4: 'lightgrey'}
    
    # Draw each piece based on the solution
    for idx, (piece_idx, rotation) in enumerate(solution):
        row, col = divmod(idx, l)
        x, y = col, h - row - 1  # Adjust y for top-left origin

        # Rotate the piece according to its orientation
        piece = pieces[piece_idx]
        piece = piece.rotate(rotation)

        # Draw the diagonals and labels
        draw_piece(ax, piece, position=(x, y), size=1)

    plt.gca().invert_yaxis()  # Invert the y-axis to match image orientation
    plt.title('Affichage du puzzle pour la meilleure solution des 10 runs ')
    plt.show()


def Affichage_resultats(list_of_best_solutions):
    # Récupération des fitness
    fitness_values = [solution[1] for solution in list_of_best_solutions]

    # Calcul de la moyenne et de l'écart type
    average_fitness = np.mean(fitness_values)
    std_dev_fitness = np.std(fitness_values)

    # Recherche de la meilleure et de la pire solution
    best_fitness = max(fitness_values)
    worst_fitness = min(fitness_values)

    # Index de la meilleure et de la pire solution
    best_index = fitness_values.index(best_fitness)
    worst_index = fitness_values.index(worst_fitness)

    # Création de la figure
    plt.figure(figsize=(10, 6))

    # Tracer les fitness
    plt.plot(range(1, len(fitness_values)+1), fitness_values, color='blue', label='Fitness')

    # Afficher la meilleure solution en vert avec un point plus gros
    plt.scatter(best_index + 1, best_fitness, color='green', label=f'Meilleure solution: {best_fitness}', s=130)

    # Afficher la pire solution en rouge avec un point plus gros
    plt.scatter(worst_index + 1, worst_fitness, color='red', label='Pire solution', s=130)

    # Afficher la moyenne en bleu
    plt.axhline(y=average_fitness, color='blue', linestyle='--', label=f'Moyenne: {average_fitness:.2f} ± {std_dev_fitness:.2f}')

    # Ajouter des titres et des étiquettes
    plt.title('Résultats des meilleurs solutions pour chaque run')
    plt.xlabel('Algorithmes génétique')
    plt.ylabel('Best fitness')
    plt.legend()

    # Afficher
    plt.grid(True)
    plt.show()
