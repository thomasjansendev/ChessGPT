class Piece:
    def __init__(self, color: str) -> None:
        self.color = color
        self.id = "n/a"
        
    def get_position(self, board: list):
        pass
    
    
class Queen(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.id = "Q"

class King(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.id = "K"
        
class Knight(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.id = "N"

class Bishop(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.id = "B"

class Rook(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.id = "R"

class Pawn(Piece):
    def __init__(self, color: str) -> None:
        super().__init__(color)
        self.id = "p"