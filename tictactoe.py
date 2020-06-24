#Defining the player class for each player in the game
class player:
    #Initializer for each player object with corresponding name, symbol, array of moves, and number of wins
    def __init__(self, name, symbol, moves):
        self.name = name
        self.symbol = symbol
        self.moves = moves
        self.numWins = 0

    #Function that prints the information of each player
    def printInfo(self):
        print("Name: " + self.name)
        print("Symbol: " + self.symbol)
        print("Wins: %s" % self.numWins + "\n")

#Defining the game class that operates the tictactoe game
class game:
    #Initializes the game board as a dictionary with 9 entries that are empty by default
    def __init__(self):
        self.board = {'1': ' ', '2': ' ', '3': ' ',
                 '4': ' ', '5': ' ', '6': ' ',
                 '7': ' ', '8': ' ', '9': ' '}
        self.board_keys = []
        for key in self.board:
            self.board_keys.append(key)

    #Function that resets the game
    def resetGame(self, player1, player2):
        #Resets each square of the board by setting the value to empty
        for key in self.board_keys:
            self.board[key] = " "
        #Clears the moves array of each player
        player1.moves.clear()
        player2.moves.clear()

    #Function that displays the board
    def printBoard(self):
        print(self.board['1'] + "|" + self.board['2'] + "|" + self.board['3'])
        print("-+-+-")
        print(self.board['4'] + "|" + self.board['5'] + "|" + self.board['6'])
        print("-+-+-")
        print(self.board['7'] + "|" + self.board['8'] + "|" + self.board['9'])
        print("\n")

    #Function that prints the default board for users to understand the layout of the board
    def printBlankBoard(self) :
        print("Default Board:\n")
        print('1' + "|" + '2' + "|" + '3')
        print("-+-+-")
        print('4' + "|" + '5' + "|" + '6')
        print("-+-+-")
        print('7' + "|" + '8' + "|" + '9')
        print("\n")

    #Prints the final board after the game has concluded
    def printFinalBoard(self):
        print("Final Board: ")
        self.printBoard()
        print("\n")

    #Function that handles the turns for each player
    #Returns true for a successful turn, returns false otherwise
    def turn(self, player):
        #Defines a variable as the players input of a desired space on the board
        move = input(player.name + "'s turn, choose a spot to place your symbol\n")
        #Conditional that ensures the player is entering a number between 1 and 9
        if move.isdigit() == False or int(move) > 9 or int(move) < 0:
            print("Invalid selection, please choose a correct space")
            return False
        #Conditional that checks if the desired spot is empty
        elif self.board[move] == ' ':
            #Places the players symbol in the specified spot on the board
            self.board[move] = player.symbol
            #Appends the spot to the players moves array
            player.moves.append(int(move))
            #Prints the board to show where the user entered their symbol
            self.printBoard()
            return True
        #Conditional that handles the case of the spot being filled
        else:
            print("That spot is already filled. Choose a spot to place your symbol\n")
            return False

    #Function that checks if a specified player has won the game
    #Returns true if a winnning pair of 3 has been located in the players moves array and false otherwise
    def checkWin(self, player):
        #Range of conditionals that checks if the players moves array contains
        #spots that indicate a win, increments the corresponding players
        #number of wins if one has been detected
        if 1 in player.moves and 2 in player.moves and 3 in player.moves:
            player.numWins += 1
            return True
        elif 4 in player.moves and 5 in player.moves and 6 in player.moves:
            player.numWins += 1
            return True
        elif 7 in player.moves and 8 in player.moves and 9 in player.moves:
            player.numWins += 1
            return True
        elif 1 in player.moves and 5 in player.moves and 9 in player.moves:
            player.numWins += 1
            return True
        elif 3 in player.moves and 5 in player.moves and 7 in player.moves:
            player.numWins += 1
            return True
        elif 1 in player.moves and 4 in player.moves and 7 in player.moves:
            player.numWins += 1
            return True
        elif 2 in player.moves and 5 in player.moves and 8 in player.moves:
            player.numWins += 1
            return True
        elif 3 in player.moves and 6 in player.moves and 9 in player.moves:
            player.numWins += 1
            return True
        else:
            return False

    #Function that handles the order that the game is played in
    def playGame(self, Player1, Player2):
        #Prints each players information accordingly
        print("\nPlayer 1:")
        Player1.printInfo()
        print("Player 2:")
        Player2.printInfo()
        self.printBlankBoard()
        #Count variable that keeps track of how many turns have been played
        count = 0
        #While loop that only occurs 9 times (one turn for each square)
        while count < 9:
            #Conditional that checks if either player has won after 5 turns
            if count >= 5 and self.checkWin(Player1) or self.checkWin(Player2):
                break
            #Player 1's turn when count is an even number
            #Conditional that checks if a successful turn has been made by player 1
            if count % 2 == 0 and self.turn(Player1):
                #Incrementing count once the turn has been successfully made
                count += 1
            #Conditional that checks if a successful turn has been made by player 1
            elif count % 2 != 0 and self.turn(Player2):
                #Incrementing count once the turn has been successfully made
                count += 1
            #If an unsuccessful move has been made by either player, the while loop
            #will continue and prompt the user for another turn
            else:
                continue
        #Conditional that checks if 9 moves have been made without either player winning
        if count == 9 and not self.checkWin(Player1) and not self.checkWin(Player2):
            print("Game Over! It's a tie!\n")
        #Conditional that runs if a player has won
        else:
            print("Winner!\n")
            #Invokes the printFinalBoard function to print the final board
            self.printFinalBoard()
        #Input request if the player wants to play another game
        restart = input("Do you want to play again? (Y/N)\n")
        #If the player has indicated that they would like to play again, the
        #resetGame function is invoked and the playGame function starts another game
        if restart == "y" or restart == "Y":
            self.resetGame(Player1, Player2)
            self.playGame(Player1, Player2)

#Defining the class that will run the tictactoe game
class main:
    #Input prompts for each player 1's desired name and symbol
    playerName = input("Player 1, please enter your name:\n")
    playerSymbol = input("Player 1, enter your desired symbol. Press Enter for default:")
    #Default symbol for Player 1
    if playerSymbol == "":
        print("Default\n")
        playerSymbol = "X"
    #Empty array for Player 1's moves array
    playerMoves = []
    #Creates a player object for player 1 with their desired name, symbol, and an empty moves array
    Player1 = player(playerName, playerSymbol, playerMoves)
    #Input prompts for each player 2's desired name and symbol
    playerName = input("Player 2, please enter your name:\n")
    playerSymbol = input("Player 2, enter your desired symbol. Press Enter for default:")
    #Default symbol for Player 1
    if playerSymbol == "":
        print("Default\n")
        playerSymbol = "O"
    #Empty array for Player 2's moves array
    playerMoves = []
    #Creates a player object for player 2 with their desired name, symbol, and an empty moves array
    Player2 = player(playerName, playerSymbol, playerMoves)
    #Creates a game object for player 1 and player 2 to play on
    currGame = game()
    #Invokes the playGame function on the game object for player 1 and player 2
    currGame.playGame(Player1, Player2)
