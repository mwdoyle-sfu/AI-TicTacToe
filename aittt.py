"""
    Assignment 3
    Matthew Doyle
    301322233
    mwdoyle@sfu.ca
    
    A program so play tic-tac-toe against an AI which uses pure monte-carlo-tree search (MCTS)
"""

import random

def alternate(activePlayer):
    if (activePlayer == 2):
        activePlayer = 1
    else:
        activePlayer = 2
    return activePlayer

def make_move(player_move, current_player, gameboard):
    gameboard[player_move] = int(current_player)
    return gameboard

def ai_move(current_player, gameboard):
    # get legal moves
    legal_moves = []
    for i in range(9):
        if gameboard[i] == 0:
            legal_moves.append(i)

    # create datastructure for winning moves
    move_win_count = {}
    for move in legal_moves:
        move_win_count[move] = 0

    # make random play outs
    for move in legal_moves:
        for i in range(10000):
            move_win_count[move] += play_out(move, current_player, gameboard)

    # find and make chosen move
    move_choice = legal_moves[0]
    choiceWinCount = move_win_count[move_choice]
    for win in move_win_count:
        if move_win_count[win] >= choiceWinCount:
            move_choice = win
            choiceWinCount = move_win_count[win]
    gameboard = make_move(int(move_choice), current_player, gameboard)
    print("AI move:", move_choice)
    return gameboard

def play_out(move, current_player, gameboard):
    # copy the gameboard
    gameboard_copy = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    gameboard_copy = gameboard.copy()

    # play the game out
    gameboard_copy = make_move(move, current_player, gameboard_copy)
    while (game_active(gameboard_copy)):
        current_player = alternate(current_player)
        legal_moves = []
        for i in range(9):
            if gameboard_copy[i] == 0:
                legal_moves.append(i)
        random_move = random.randint(0, 8)
        while (random_move not in legal_moves):
            random_move = random.randint(0, 8)
        gameboard_copy = make_move(random_move, current_player, gameboard_copy)
    
    # return the winning heuristics
    if (game_result(gameboard_copy) == 2):
        return 4
    elif (game_result(gameboard_copy) == 1):
        return -2
    else:
        return 1

def game_active(gameboard):
    active_game = False
    if game_result(gameboard) == -1:
        active_game = True
    return active_game

def game_result(gameboard):
    # search for winner
    players = [1, 2]
    for player in players:
        # win at 0 3 6
        if all(v == player for v in gameboard[::3]):
            return(player)
        # win at 1 4 7
        if all(v == player for v in gameboard[1::3]):
            return(player)   
        # win at 2 5 8
        if all(v == player for v in gameboard[2::3]):
            return(player) 
        # win at 0 1 2
        if all(v == player for v in gameboard[:3:]):
            return(player)
        # win at 3 4 5
        if all(v == player for v in gameboard[3:6:]):
            return(player)
        # win at 6 7 8
        if all(v == player for v in gameboard[6::]):
            return(player)
            # win at 0 4 8
        if all(v == player for v in gameboard[::4]):
            return(player)
        # win at 2 4 6
        if all(v == player for v in gameboard[2:8:2]):
            return(player)
    # draw
    if all(v != 0 for v in gameboard):
        return(0)
    # game not over
    return(-1)    

def print_menu():
    print("Choose from the following")
    print("0 1 2 \n3 4 5\n6 7 8")

def print_board(gameboard):
    board = ['- ', '- ', '- ', '- ', '- ', '- ', '- ', '- ', '- ']
    display_board = ''
    for i in range(len(gameboard)):
        if gameboard[i] == 1:
            board[i] = 'X '
        if gameboard[i] == 2:
            board[i] = 'O '
        if i == 2 or i == 5:
            display_board += (board[i] + '\n')
        else:
            display_board += board[i]
    print(display_board)

def print_game_over(gameboard, in_game):
    if (game_result(gameboard) == 0):
        print("** Draw Game **")
        in_game = False
    if (game_result(gameboard) == 1):
        print("** Player Wins **")
        in_game = False
    if (game_result(gameboard) == 2):
        print("** AI Wins **")
        in_game = False
    return in_game

def play_a_new_game():
    print("Starting the game...")
    gameboard = [0, 0, 0, 0, 0, 0, 0, 0, 0]
    current_player = 1
    in_game = True
    player_move = ''

    # ask player or AI first
    choice = input('Would you like to go first(y/n)? : ')
    if choice.upper() == 'N':
        current_player = alternate(current_player)

    # start game
    while in_game == True:
        if current_player == 1:
            print_menu()
            player_move = input('Player move: ')
            gameboard = make_move(int(player_move), current_player, gameboard)
            print_board(gameboard)
        else:
            print("AI is thinking...")
            gameboard = ai_move(current_player, gameboard)
            print_board(gameboard)

        current_player = alternate(current_player)
        in_game = print_game_over(gameboard, in_game)

if __name__ == '__main__':
    play_a_new_game()
