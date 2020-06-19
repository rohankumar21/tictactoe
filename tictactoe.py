#Initializing the board to a 3x3 dictionary
board = {'1': ' ', '2': ' ', '3': ' ',
         '4': ' ', '5': ' ', '6': ' ',
         '7': ' ', '8': ' ', '9': ' '}

#Initializing every space in the dictionary to an empty space
board_keys = []

for key in board:
    board_keys.append(key)

#Function that displays the board
def printBoard() :
    print(board['1'] + "|" + board['2'] + "|" + board['3'])
    print("-+-+-")
    print(board['4'] + "|" + board['5'] + "|" + board['6'])
    print("-+-+-")
    print(board['7'] + "|" + board['8'] + "|" + board['9'])

#Function that returns whether the current player has won or not
def checkWin(turn):
    win = False
    #Conditionals that check every consecutive triple that denotes a win
    if board['1'] == board['2'] == board['3'] != ' ': # across the top
        win = True
    elif board['4'] == board['5'] == board['6'] != ' ': # across the middle
        win = True
    elif board['7'] == board['8'] == board['9'] != ' ': # across the bottom
        win = True
    elif board['1'] == board['4'] == board['7'] != ' ': # down the left side
        win = True
    elif board['2'] == board['5'] == board['8'] != ' ': # down the middle
        win = True
    elif board['3'] == board['6'] == board['9'] != ' ': # down the right side
        win = True
    elif board['3'] == board['5'] == board['7'] != ' ': # diagonal
        win = True
    elif board['1'] == board['5'] == board['9'] != ' ': # diagonal
        win = True
    return win

#Function that interacts with the user
def game() :
    #User input for the desired symbol of the player
    player1 = input("Player 1, enter your desired symbol. Press Enter for default\n")
    #Default symbol for Player 1
    if player1 == "":
        player1 = "X"
        print("Player 1: X")
    #User input for the desired symbol of the player
    player2 = input("Player 2, enter your desired symbol. Press Enter for default\n")
    #Default symbol for Player 2
    if player2 == player1:
        player2 = input("Invalid symbol entered, please enter a different symbol. Press Enter for default\n")
    if player2 == "":
        player2 = "O"
        print("Player 2: O")
    #Integer that tracks the number of plays that have occurred
    count = 0;
    #Boolean that tracks which users turn it is
    flag = True
    #While loop that iterates 9 times (limit based on size of board)
    while count < 9:
        #Prints the current board for every turn
        printBoard()
        #Conditional for Player 1's turn
        if flag:
            move = input("Player 1's turn, choose a spot to place your symbol\n")
            #Checks if the desired space is empty
            if move.isdigit() == False or int(move) > 9 or int(move) < 0:
                print("Invalid selection, please choose a correct space")
                continue
            elif board[move] == ' ':
                #Places player 1's symbol in the correct spot
                board[move] = player1
                #Increments the number of plays that have occurred
                count += 1
            else:
                print("That spot is already filled. Choose a spot to place your symbol\n")
                continue
            if count >= 3 and checkWin(player1):
                print("Player 1 Wins!\n")
                print("\n" + "Final Board:")
                printBoard()
                print("\n")
                break
            flag = False
        else:
            move = input("Player 2's turn, choose a spot to place your symbol\n")
            if move.isdigit() == False or int(move) > 9 or int(move) < 0:
                print("Invalid selection, please choose a correct space")
                continue
            elif board[move] == ' ':
                board[move] = player2
                count += 1
            else:
                print("That spot is already filled. Choose a spot to place your symbol\n")
                continue
            if count >= 3 and checkWin(player2):
                print("Player 2 Wins!\n")
                print("\n" + "Final Board:")
                printBoard()
                print("\n")
                break
            flag = True
    if count == 9 and not checkWin(player2) or not checkWin(player1):
        print("Game Over! It's a tie!\n")
    restart = input("Do you want to play again? (Y/N)\n")
    if restart == "y" or restart == "Y":
        for key in board_keys:
            board[key] = " "
        game()
game()
