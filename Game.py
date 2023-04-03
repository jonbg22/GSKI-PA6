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
        self.pass_counter = 0

    def init_word_list(self):
        """
        Fetches dictionary from file into word list
        """
        with open(self.DICTIONARYFILE,"r",encoding="UTF-8") as f:
            lines = f.readlines()
            for line in lines:
                word = line.strip().split("\t")[0].strip()
                self.WORD_LIST.append(word)

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
        """
        Returns the player object of the current player
        """
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
                self.pass_counter = 0

            case 2: # Swap Letters
                self.swap_letters(player)
                self.pass_counter = 0

            case 3: # Pass Turn
                self.pass_counter += 1
        player.hand = player.hand + self.draw(7-len(player.hand)) # Draws up to 7 letter

    def place_word(self,player):
        """
        Allows player to place a word formed from his letters
        """
        print(f"Your Letters: {' '.join(player.hand)}")
        while True:
            # Gets and validates all player input
            while True:
                flag = True
                word = input("Enter word you want to place: ")
                if len(word) == 0:
                    print("Invalid Input, try again")
                    flag = False
                if flag:
                    break
            
            while True:
                rowPos,colPos = map(int,input("Enter position for start of word (row,col): ").split(","))
                if rowPos == None or colPos == None:
                    print("Invalid Input, try again")
                    continue
                break
            
            while True:
                direction = input("Enter direction for word to go (R (Right),D (Down)): ")
                if direction.upper() not in ["R","D"]:
                    print("Invalid Input, try again")
                    continue
                break 

            # Attempts to add word to a copy of the board to verify placement
            copy_board = Board()
            copy_board.board = deepcopy(self.board.board)
            copy_board.empty = self.board.empty
            response = copy_board.add_word(rowPos-1,colPos-1,direction,word,self.points_map,deepcopy(player.hand))
            if response == "Not Center":
                print("First word placed needs to pass over center tile")
                continue
            elif response == False and all([self.validate_word(word) for word in copy_board.get_all_words_on_board()]):
                print("Invalid placement, turn forfeitted")
                sleep(2) # Sleeps to give time for prompt to be visible
                break
            else:
                letters_used,word_score = self.board.add_word(rowPos-1,colPos-1,direction,word,self.points_map,deepcopy(player.hand))
                if len(word) == 7:
                    word_score += 50 # 7 Letter Bonus
                player.score += word_score
                self.board.empty = False
                for letter in letters_used:
                    try:
                        player.hand.remove(letter.upper())
                    except ValueError:
                        player.hand.remove("*")
                print(f"The word { word.upper() } was successfully added to the board giving {word_score} points. New Score: {player.score}")
            del copy_board
            break

    def swap_letters(self,player):
        """
        Allows player to swap letters from his hand with new ones from the bag
        """
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
                picked_letter = input(f"Choose letter to swap, {amount-n} choices left: ")   
                try:
                    new_hand.remove(picked_letter) 
                    break
                except ValueError:
                    print("Please input a valid letter from your hand: ")
        player.hand = new_hand + self.draw(amount)
        print("New Hand:"," ".join(player.hand))
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
        """
        Returns True if word is in the word dictionary
        """
        return word.upper() in self.WORD_LIST

    def check_game_over(self):
        """
        Returns true if bag is empty and one of the players has an empty hand, which signals it is game over
        """
        return len(self.bag) == 0 and any([len(player.hand) == 0 for player in self.players]) or self.pass_counter >= self.playercount*2

    def __main(self):
        """
        Main game loop
        """
        while self.started:
            cur_player = self.get_current_player()
            self.board.print_board()
            print(f"It is {cur_player.name}'s Turn (score: {cur_player.score})")
            self.start_turn()
            if self.check_game_over():
                self.started = False
                print("Game Over! \nFinal Scores:")
                for player in self.players:
                    print(f"Player {player.name} with score {player.score}")
                break
            self.next_turn()


if __name__ == "__main__":
    g = Game(2)
    from Player import Player
    g.add_player(Player("Nonni"))
    g.add_player(Player("Adam"))
    g.start_game()
    
