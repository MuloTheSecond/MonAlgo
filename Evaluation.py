import abc

""" On va en faire une classe abstraite"""
class Evaluation(abc.ABC):
    
    def __init__(self):
        pass  # Vous pouvez initialiser des attributs ici si nécessaire
    

    @staticmethod
    def evaluate_solution(l, h, pieces, solution):
        """Vérification de validité :"""
        for i in range(l):
            if pieces[solution[i][0]][(6 - solution[i][1]) % 4] != 0:
                return -1  
        for i in range(l * (h - 1), l * h):
            if pieces[solution[i][0]][(4 - solution[i][1]) % 4] != 0:
                return -1  
        for i in range(0, l * h, l):
            if pieces[solution[i][0]][(5 - solution[i][1]) % 4] != 0:
                return -1  
        for i in range(l - 1, l * h, l):
            if pieces[solution[i][0]][(3 - solution[i][1]) % 4] != 0:
                return -1  

        """Calcul du score de performance :"""
        result = 0
        for i in range(l * h - 1):
            if i % l != l - 1:  
                if pieces[solution[i][0]][(3 - solution[i][1]) % 4] == \
                pieces[solution[i + 1][0]][(5 - solution[i + 1][1]) % 4]:
                    result += 1
        for i in range(l * (h - 1)):
            if pieces[solution[i][0]][(4 - solution[i][1]) % 4] == \
            pieces[solution[i + l][0]][(6 - solution[i + l][1]) % 4]:
                result += 1
        return result
    
    @staticmethod
    def evaluateBorders(l, h, pieces, solution):
   
        result = 0
        for i in range(l):  # Vérifie le bord supérieur
            if pieces[solution[i][0]][(6 - solution[i][1]) % 4] == 0:
                result += 1

        for i in range(l * (h - 1), l * h):  # Vérifie le bord inférieur
            if pieces[solution[i][0]][(4 - solution[i][1]) % 4] == 0:
                result += 1

        for i in range(0, l * h, l):  # Vérifie le bord gauche
            if pieces[solution[i][0]][(5 - solution[i][1]) % 4] == 0:
                result += 1

        for i in range(l - 1, l * h, l):  # Vérifie le bord droit
            if pieces[solution[i][0]][(3 - solution[i][1]) % 4] == 0:
                result += 1
        print(result)
        return result


    @staticmethod
    def print_puzzle_state(l, h, solution):
        """Affiche l'état du puzzle"""
        print("Puzzle State:")
        for i in range(h):
            for j in range(l):
                pos = i * l + j
                piece_idx, rotation = solution[pos]
                print(f"{piece_idx:2d}@{rotation}", end=' ')
            print()  
        print() 
