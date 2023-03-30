from Game import Game
from Player import Player

while True:
    try:
        playercount = int(input("Enter playercount (2-4): "))
        if playercount < 2 or playercount > 4:
            raise ValueError
        break
    except (ValueError, TypeError):
        print("Incorrect Input")

game = Game(playercount)

for player_number in range(playercount):
    while True:
        name = input(f"Player {player_number+1} Name: ")
        if len(name) == 0: print("Name is too short")
        elif len(name) > 24: print("Name is too long")
        else:
            break
    game.add_player(Player(name))


game.start_game()





