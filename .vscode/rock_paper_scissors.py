import random

rps_dict = {'1':'Rock O', '2':'Paper []', '3':'Scissor X'}

comp_wins = 0
player_wins = 0 

def win_loss_decider(player, comp):
    if player == comp:
        return 0 #Tie
    else:
        if int(player) - int(comp) == 1 or (player == '1' and comp =='3'):
            return 1 #Player Win
        else:
            return -1 #Computer Win
        


while True:
    player = input("R-1/P-2/S-3 (or END)")
    computer = str(random.randint(1,3))

    if player == "END": 
        print(f"Player wins: {player_wins}")
        print(f"Computer wins: {comp_wins}")
        break

    result = win_loss_decider(player, computer)


    print("=================")
    print(f"Player: {rps_dict[player]}")
    print(f"Computer: {rps_dict[computer]}")
    print("\n")
    if result == 1 : 
        print("Player Wins!")
        player_wins += 1
    elif result == -1: 
        print("Computer Wins!")
        comp_wins += 1
    else: print("It's a tie!")


    print("=================\n\n")
