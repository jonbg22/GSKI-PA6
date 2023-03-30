class Player:
    def __init__(self,name) -> None:
        self.name = name
        self.hand = [] 
        self.score = 0

    def add_to_hand(self,letters):
        """
        Adds letters to player hand
        """
        [self.hand.append(letter) for letter in letters]
