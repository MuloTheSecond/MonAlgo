class Piece:
    def __init__(self, bottom: int, left: int, top: int, right: int):
        """
        Initialise une instance de la classe Piece avec les bords spécifiés.

        Args:
        - bottom, left, top, right (int) : valeurs des bords
        """
        self.edges = [bottom, left, top, right]
    
    def __getitem__(self, index: int) -> int:
        """
        Overwrite de l'opérateur [] pour nous permettre d'accéder à un bord spécifique de la pièce en utilisant l'opérateur [].

        Args:
        - index (int): L'index du bord (0: bottom, 1: left, 2: top, 3: right).

        Returns:
        - int: La valeur du bord correspondant à l'index spécifié.
        """
        return self.edges[index]
    
    def estGauche(self) -> bool:
        """
        Vérifie si la pièce est placée sur le bord gauche du puzzle.

        Returns:
        - bool: True si la pièce est sur le bord gauche, False sinon.
        """
        return self.edges[1] == 0
    
    def estDroite(self) -> bool:
        """
        Vérifie si la pièce est placée sur le bord droit du puzzle.

        Returns:
        - bool: True si la pièce est sur le bord droit, False sinon.
        """
        return self.edges[3] == 0
    
    def estHaut(self) -> bool:
        """
        Vérifie si la pièce est placée sur le bord supérieur du puzzle.

        Returns:
        - bool: True si la pièce est sur le bord supérieur, False sinon.
        """
        return self.edges[2] == 0
    
    def estBas(self) -> bool:
        """
        Vérifie si la pièce est placée sur le bord inférieur du puzzle.

        Returns:
        - bool: True si la pièce est sur le bord inférieur, False sinon.
        """
        return self.edges[0] == 0

    def rotate(self, times: int) -> list[int]:
        """
        Effectue une rotation des bords de la pièce un certain nombre de fois.
        Args:
        - times (int): Le nombre de rotations à effectuer.
        Returns:
        - list[int]: Une liste représentant les bords de la pièce après rotation.
        """
        times = times % 4
        return self.edges[-times:] + self.edges[:-times]  
    
    def __repr__(self) -> str:
        """
        Returns:
        - str: Représentation de chaîne de la pièce.
        """
        return f"Piece(edges={self.edges})"
    
    def is_corner_piece(self):
        return self.edges.count(0) == 2


    def is_edge_piece(self):
        return self.edges.count(0) == 1