class Square:
    def __init__(self, solid, ledge) -> None:
        self.solid = solid
        self.ledge = ledge

    def __repr__(self) -> str:
        char = 'O'
        if self.is_solid():
            char = 'X'
        elif self.is_ledge():
            char = 'I'

        return char

    def is_solid(self):
        return self.solid

    def ledge_exists(self):
        return self.ledge is not None
    
    def is_jumping_ledge(self, direction):
        return self.ledge_exists() and self.ledge == direction

    def is_blocking_ledge(self, direction):
        return self.ledge_exists() and self.ledge != direction
