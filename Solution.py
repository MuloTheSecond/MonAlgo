from Problem import Problem
import Affichage


def main():

    """ Ensemble des paramètres modifiables :"""
    # 100k évaluations -- > 100*1000
    population_size = 100
    generations =  1000
    mutation_rate = 0.03
    temperature = 120
    cooling_rate = 0.95
    tournament_size = 50

    list_of_best_solutions = []



    """DEBUT partie a modifier -- > Chemin d'accès du bench"""
    nb_runs = 1 
    l, h, pieces = Problem.load_puzzle(r'C:\Users\MathieuPhil\Documents\Travail\IMT\M1\MAD\Puzzle\Docs_Eternity\benchs\pieces_set\pieces_16x16.txt')
    
    """FIN partie à modifier"""



    for loop in range(nb_runs):   
        best_solution, best_fitness = Problem.genetic_algorithm(l, h, pieces, population_size=population_size, generations=generations, mutation_rate=mutation_rate, temperature = temperature, cooling_rate = cooling_rate, tournament_size=tournament_size)
        list_of_best_solutions.append((best_solution,best_fitness))
    solution_ultime = (best_solution, best_fitness)
    for loop in range(nb_runs):
        if list_of_best_solutions[loop][1] > solution_ultime [1] :
            solution_ultime = list_of_best_solutions[loop]

    Affichage.Affichage_resultats(list_of_best_solutions)
    Affichage.draw_full_puzzle(pieces, solution_ultime[0], l, h)




if __name__ == "__main__":
    main()


