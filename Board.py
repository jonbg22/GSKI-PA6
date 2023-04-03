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
    LINE_POWERUPS_LOCATIONS = [ # The powerup locations for each line
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
    POWERUPS_RENDER = { # The format for rendering powerups on to the screen
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
        """
        Prints the board
        Shows '-' if tile is empty
        Displays the letter if square is not empty
        If the square is empty but has a powerup, that powerup is shown according to POWERUPS_RENDER
        """
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
        """
        Goes through the board by row and by column
        And returns all words found
        """
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

    def add_word(self,startRow,startCol,direction,word,points_map,playerHand):
        """
        Adds word to board letter by letter
        Returns false if placement would override another word
        Returns "Not Center" if no word has been placed and word does not go through center
        """
        match direction.upper(): # Get direction to step in list
            case "R":
                step = (0,1)
            case "D":
                step = (1,0)
            case _:
                raise ValueError
        word_multipliers = []
        score = 0
        hits_center = False # Will be true if word passes over center of board
        intersects_word = False # Will be True if word goes through another word on board
        letters_used = list(word) 
        posRow,posCol = startRow,startCol
        for letter in word:
                try:
                    if self.board[posRow][posCol].letter != None:
                        intersects_word = True
                    else:
                        try:
                            playerHand.remove(letter.upper())
                        except ValueError:
                            if "*" in playerHand:
                                playerHand.remove("*")
                            else:
                                raise InvalidPlacement
                    multiplier = self.add_letter(posRow,posCol,letter)
                    if posRow == 7 and posCol == 7:
                        hits_center = True
                    letter_points = points_map[letter.upper()]
                    if multiplier == Powerup.DOUBLELETTER:
                        letter_points *= 2
                    elif multiplier == Powerup.TRIPLELETTER:
                        letter_points *= 3
                    else:
                        word_multipliers.append(multiplier)
                    score += letter_points
                    posRow += step[0]
                    posCol += step[1]
                except InvalidPlacement:
                    return False
        if self.empty and not hits_center:
            return "Not Center"
        if not intersects_word and not self.empty:
            return False

        for mult in word_multipliers:
            if mult == Powerup.DOUBLEWORD:
                score *= 2
            elif mult == Powerup.TRIPLEWORD:
                score *= 3
        return letters_used, score

    def add_letter(self,rowPos,colPos,letter):
        """
        Adds given letter to position on board
        Raises InvalidPlacement Error if placement is illegal
        """
        target_pos = self.board[rowPos][colPos]
        # print("Placing Letter",letter,"At",target_pos.letter)
        if target_pos.letter != None and target_pos.letter != letter.upper():
            raise InvalidPlacement
        if rowPos < 0 or rowPos >= self.height or colPos < 0 or colPos >= self.width:
            raise InvalidPlacement
        self.board[rowPos][colPos].letter = letter.upper() 
        return self.board[rowPos][colPos].powerup
        