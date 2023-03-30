class Square:
    def __init__(self,letter=None, powerup = None) -> None:
        self.letter = letter
        self.powerup = powerup

    def __str__(self) -> str:
        if self.letter == None:
            return '-'
        return str(self.letter)