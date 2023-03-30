from Square import Square
from enum import Enum

class InvalidPlacement(Exception):
    pass

class Powerup(Enum):
    DOUBLELETTER = 1,
    TRIPLELETTER = 2,
    DOUBLEWORD = 3,
    TRIPLEWORD = 4,
    CENTER = 5

class Board:
    LINE_POWERUPS_LOCATIONS = [
        {0: Powerup.TRIPLEWORD,3: Powerup.DOUBLELETTER,7:Powerup.TRIPLEWORD,11:Powerup.DOUBLELETTER,14:Powerup.TRIPLELETTER},
        {1: Powerup.DOUBLEWORD,13:Powerup.DOUBLEWORD},
        {2: Powerup.DOUBLEWORD,12:Powerup.DOUBLEWORD},
        {0:Powerup.DOUBLELETTER,3: Powerup.DOUBLEWORD,11:Powerup.DOUBLEWORD,14:Powerup.DOUBLELETTER},
        {4: Powerup.DOUBLEWORD,10:Powerup.DOUBLEWORD},
        {1: Powerup.TRIPLELETTER,5:Powerup.TRIPLELETTER,9:Powerup.TRIPLELETTER,13:Powerup.TRIPLELETTER},
        {2: Powerup.DOUBLELETTER,6:Powerup.DOUBLELETTER,8:Powerup.DOUBLELETTER,12:Powerup.DOUBLELETTER},
        
        {0: Powerup.TRIPLEWORD,3:Powerup.DOUBLELETTER,7:Powerup.CENTER,11:Powerup.DOUBLELETTER,14:Powerup.TRIPLEWORD},
        
        {2: Powerup.DOUBLELETTER,6: Powerup.DOUBLELETTER,8:Powerup.DOUBLELETTER,12:Powerup.DOUBLELETTER},
        {1: Powerup.TRIPLELETTER,5: Powerup.TRIPLELETTER,9: Powerup.TRIPLELETTER,13: Powerup.TRIPLELETTER},
    	{4: Powerup.DOUBLEWORD,10:Powerup.DOUBLEWORD},
        {0: Powerup.DOUBLELETTER,3:Powerup.DOUBLEWORD,11:Powerup.DOUBLEWORD,14:Powerup.DOUBLELETTER},
        {2: Powerup.DOUBLEWORD,12:Powerup.DOUBLEWORD},
        {1: Powerup.DOUBLEWORD,13:Powerup.DOUBLEWORD},
        {0: Powerup.TRIPLEWORD,3:Powerup.DOUBLELETTER,7: Powerup.TRIPLEWORD,11: Powerup.DOUBLELETTER,14:Powerup.TRIPLEWORD}

    ]
    POWERUPS_RENDER = {
        Powerup.DOUBLELETTER: "*2",
        Powerup.TRIPLELETTER: "*3",
        Powerup.DOUBLEWORD: "$2",
        Powerup.TRIPLEWORD: "$3",
        Powerup.CENTER: "0"
        }
    def __init__(self) -> None:
        self.width = 15
        self.height = 15
        self.board = self.init_board()
        self.empty = True

    def print_board(self):
        print("\n"+f"{'':<5s}",end="") # Padding for header
        for x in range(1,self.width+1): # Prints header
            print(f"{str(x):^2s}",end=" ")
        print("\n\n")
        for line_num, line in enumerate(self.board):
            print(f"{line_num+1:<4n}",end=" ")
            for square_num,square in enumerate(line):
                if square.powerup != None and square.letter == None:
                    print(f"{self.POWERUPS_RENDER[square.powerup]:^2s}",end=" ")
                else:
                    print(f"{str(square):^2s}",end=" ")
            print()
        print()

    def init_board(self):
        """
        Fills the board with Squares with powerups in the appropriate places 
        """
        board =  [[Square() for _ in range(self.width)] for _ in range(self.height)]
        for line_num,line in enumerate(self.LINE_POWERUPS_LOCATIONS):
            for power in line:
                board[line_num][power] = Square(powerup=line[power])
        return board

    def get_all_words_on_board(self):
        words = []
        # Check all rows
        for row in self.board:
            word = ""
            for square in row:
                if square.letter == None:
                    if len(word) > 1:
                        words.append(word)
                        word = ""
                    else:
                        word = ""
                else:
                    word += square.letter
        
        # Check all columns
        for row in range(self.height):
            word = ""
            for col in range(self.width):
                square = self.board[col][row]
                if square.letter == None:
                    if len(word) > 1:
                        words.append(word)
                        word = ""
                    else:
                        word = ""
                else:
                    word += square.letter
        return words

    def add_word(self,startRow,startCol,direction,word,points_map):
        """
        Adds word to board letter by letter
        Returns false if placement would override another word
        """
        match direction.upper(): # Get direction to step in list
            case "L":
                step = (0,-1)
            case "R":
                step = (0,1)
            case "U":
                step = (-1,0)
            case "D":
                step = (1,0)
            case _:
                raise ValueError
        word_multipliers = []
        score = 0
        for letter in word:
                try:
                    multiplier = self.add_letter(startRow,startCol,letter)
                    letter_points = points_map[letter.upper()]
                    if multiplier == Powerup.DOUBLELETTER:
                        letter_points *= 2
                    elif multiplier == Powerup.TRIPLELETTER:
                        letter_points *= 3
                    else:
                        word_multipliers.append(multiplier)
                    score += letter_points
                    startRow += step[0]
                    startCol += step[1]
                except InvalidPlacement:
                    return False
        for mult in word_multipliers:
            if mult == Powerup.DOUBLEWORD:
                score *= 2
            elif mult == Powerup.TRIPLEWORD:
                score *= 3
        return score

    def add_letter(self,rowPos,colPos,letter):
        """
        Adds given letter to position on board
        Raises InvalidPlacement Error if placement is illegal
        """
        target_pos = self.board[rowPos][colPos]
        # print("Placing Letter",letter,"At",target_pos.letter)
        if target_pos.letter != None and target_pos.letter != letter:
            raise InvalidPlacement
        if rowPos < 0 or rowPos >= self.height or colPos < 0 or colPos >= self.width:
            raise InvalidPlacement
        self.board[rowPos][colPos].letter = letter.upper() 
        return self.board[rowPos][colPos].powerup
        



if __name__ == "__main__":
    b = Board()
    b.print_board()
    rowPos,colPos = 1,1
    words = ["Boot","Run","Lice"]
    positions = [
        ((5,5),"L"),
        ((1,1),"D"),
        ((8,4),"U")
    ]

    for ind,word in enumerate(words):
        pos = positions[ind]
        rowPos,colPos = pos[0]
        direction = pos[1]
        print(b.add_word(rowPos-1,colPos-1,direction,word))
        b.print_board()
    print("ALL WORDS:")
    all_words = b.get_all_words_on_board()