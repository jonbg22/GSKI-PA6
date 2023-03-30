from random import randint
from Board import Board,Powerup
from time import sleep
from copy import deepcopy

class InvalidWord(Exception):
    pass

class Game:
    TURN_MENU = "1. Play Word\n2. Swap Letters\n3. Pass Turn"
    DICTIONARYFILE = "dictionary.txt"
    WORD_LIST = []

    def __init__(self,playercount) -> None:
        self.points_map = {"A": 1, "B": 3, "C": 3, "D": 2, "E":1,"F":4,"G":2,"H":4,"I":1,"J":8,"K":5,"L":1,"M":3,"N":1,"O":1,"P":3,"Q":10,"R":1,"S":1,"T":1,"U":1,"V":4,"W":4,"X":8,"Y":4,"Z":10}
        self.bag = list("**"+"E"*12+"A"*9+"I"*9+"O"*8+"N"*6+"R"*6+"T"*6+"L"*4+"S"*4+"U"*4+"D"*4+"G"*3+"B"*2+"C"*2+"M"*2+"P"*2+"F"*2+"H"*2+"V"*2+"W"*2+"Y"*2+"K"+"J"+"X"+"Q"+"Z")
        self.players = []
        self.started = False
        self.current_player = 0
        self.playercount = playercount
        self.board = Board()
        self.init_word_list()

    def init_word_list(self):
        """
        Fetches dictionary from file into word list
        """
        with open(self.DICTIONARYFILE,"r",encoding="UTF-8") as f:
            lines = f.readlines()
            for i,line in enumerate(lines):
                word = line.strip().split("\t")[0].strip()
                self.WORD_LIST.append(word)
        # print(len(self.WORD_LIST))

    def next_turn(self):
        """
        Sets current player to next player in turn order
        """
        if self.current_player == self.playercount-1:
            self.current_player = 0
        else:
            self.current_player += 1

    def add_player(self,player):
        """
        Adds a player to the game
        """
        if not self.started:
            self.players.append(player)

    def get_current_player(self):
        return self.players[self.current_player]

    def start_game(self):
        """
        Makes all players draw seven letters and starts the game
        """
        for player in self.players:
            player.add_to_hand(self.draw(7))
        self.started = True
        self.__main()

    def start_turn(self):
        """
        Performs one turn in the game with the current player
        """
        player = self.players[self.current_player]
        print(f"Your Letters: {' '.join(player.hand)}")
        print(self.TURN_MENU)
        while True:
            try:
                choice = int(input("Choose an option (1-3): "))
                if choice < 1 or choice > 3:
                    raise ValueError
                break
            except (ValueError, TypeError):
                print("Incorrect Input")

        match choice:
            case 1: # Place Word
                self.place_word(player)

            case 2: # Swap Letters
                self.swap_letters(player)

            case 3: # Pass Turn
                pass

    def get_word_score(self,word):
        """
        Returns sum of all individual letter scores of words
        """
        return sum([self.points_map[letter] for letter in word])

    def place_word(self,player):
        """
        Allows player to place a word formed from his letters
        """
        print(f"Your Letters: {' |'.join(player.hand)}")

        # Gets and validates all player input
        while True:
            word = input("Enter word you want to place: ")
            # TODO: Verify that all letters are in player's hand
            if len(word) == 0:
                print("Invalid Input, try again")
                continue
            break
        
        while True:
            rowPos,colPos = map(int,input("Enter position for start of word (row,col): ").split(","))
            print(f"Row Pos: {rowPos} Row Pos: {colPos}")
            if rowPos == None or colPos == None:
                print("Invalid Input, try again")
                continue
            break
        
        while True:
            direction = input("Enter direction for word to go (L,R,U,D): ")
            if direction.upper() not in ["L","R","U","D"]:
                print("Invalid Input, try again")
                continue
            break 

        # Attempts to add word to a copy of the board to verify placement
        copy_board = Board()
        copy_board.board = deepcopy(self.board.board)
        if copy_board.add_word(rowPos-1,colPos-1,direction,word,self.points_map) != False and all([self.validate_word(word) or self.validate_word(word[::-1]) for word in copy_board.get_all_words_on_board()]):
            word_score = self.board.add_word(rowPos-1,colPos-1,direction,word,self.points_map)
            player.score += word_score
            self.board.empty = False
            print(f"The word { word.upper() } was successfully added to the board. New Score: {player.score}")
        else:
            print("Invalid placement, turn forfeitted")
            sleep(2) # Sleeps to give time for 
        del copy_board

    def swap_letters(self,player):
        while True:
            try:
                amount = int(input("Enter amount of letters to swap: "))
                if amount <= 0 or amount > len(player.hand)-1:
                    raise ValueError
                break
            except (ValueError, TypeError):
                print("Invalid Input, try again")
        new_hand = deepcopy(player.hand)
        for n in range(amount):
            print("Your hand: "+ "".join(new_hand))
            while True:
                picked_letter = input(f"Choose letter to swap, {amount-n-1} choices left: ")   
                try:
                    new_hand.remove(picked_letter) 
                    break
                except ValueError:
                    print("Please input a valid letter from your hand: ")
        player.hand = new_hand + self.draw(amount)

    def draw(self,amount):
        """
        Draws x amount of letters from the bag and returns them in a list
        """
        pile = []
        for _ in range(amount):
            num = randint(0,len(self.bag)-1) # Picks a random index in the bag
            pile.append(self.bag.pop(num)) # Draws that letter from the bag
        return pile

    def validate_word(self,word):
        return word.upper() in self.WORD_LIST

    def check_game_over(self):
        return len(self.bag) == 0 and any([len(player.hand) == 0 for player in self.players])

    def __main(self):
        """
        Main loop
        """
        while self.started:
            cur_player = self.get_current_player()
            self.board.print_board()
            print(f"It is {cur_player.name}'s Turn (score: {cur_player.score})")
            self.start_turn()
            if self.check_game_over():
                self.started = False
                break
            self.next_turn()


if __name__ == "__main__":
    g = Game(2)
    from Player import Player
    g.add_player(Player("Nonni"))
    g.add_player(Player("Adam"))
    g.start_game()
    
