import datetime
#Defining the player class for each player in the game
class player:
    #Initializer for each player object with corresponding name, symbol, array of moves, and number of wins
    def __init__(self, name=None, symbol=None):
        self.moves = []
        self.numWins = 0
        self.name = name
        self.symbol = symbol

#Defining the game class that operates the tictactoe game
class game:
    #Initializes the game board as a dictionary with 9 entries that are empty by default
    def __init__(self):
        #Instance variable that tracks the time of the last update made to the game
        self.lastUpdate = 0
        #Instance variable for the authorization token for the current game
        self.authToken = 0
        #Player 1 and player 2 objects for the game
        #Default player objects upon instantiation
        self.player1 = player()
        self.player2 = player()
        #Instance variable that tracks which players turn it is
        self.playersTurn = player()
        #Instance variable to track how many successful moves have been made
        self.numSuccessfulTurns = 0
        #Map for the board that maps the position to the symbol present
        self.board = {1: ' ', 2: ' ', 3: ' ',
                 4: ' ', 5: ' ', 6: ' ',
                 7: ' ', 8: ' ', 9: ' '}
        self.board_keys = []
        for key in self.board:
            self.board_keys.append(key)

    #Function that returns the player object based on the name provided
    def findPlayer(self, playerName):
        if self.player1.name == playerName:
            return self.player1
        else:
            return self.player2

    #Function that resets the game
    def resetGame(self, player1, player2):
        #Resets each square of the board by setting the value to empty
        for key in self.board_keys:
            self.board[key] = " "
        #Clears the moves array of each player
        player1.moves.clear()
        player2.moves.clear()

    #Function that returns the current state of the game as a list with the symbols entered
    def getGameState(self):
        return list(self.board.values())

    #Function that displays the board
    def printBoard(self):
        print(self.board[1] + "|" + self.board[2] + "|" + self.board[3])
        print("-+-+-")
        print(self.board[4] + "|" + self.board[5] + "|" + self.board[6])
        print("-+-+-")
        print(self.board[7] + "|" + self.board[8] + "|" + self.board[9])
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

    #Function that handles the turns for each player
    #Returns true for a successful turn, returns false otherwise
    def turn(self, player, move):
        #Defines a variable as the players input of a desired space on the board
        #move = input(player.name + "'s turn, choose a spot to place your symbol\n")
        #Conditional that ensures the player is entering a number between 1 and 9
        if move > 9 or move < 1:
            raise ValueError('Invalid selection')
            #return False
        #Conditional that checks if the game has not concluded
        #if thedesired spot is empty and if it is the desired players turn
        elif not(self.checkWin(player)) and self.board[move] == ' ' and self.playersTurn.name == player.name and self.numSuccessfulTurns < 9:
            #Places the players symbol in the specified spot on the board
            self.board[move] = player.symbol
            #Appends the spot to the players moves array
            player.moves.append(move)
            #Increments the numSuccessfulTurns variable after a successful turn
            self.numSuccessfulTurns += 1
            #Conditional to check if the game has been won after the move has been successfully placed
            if self.checkWin(player):
                print(player.name + " Wins!")
                return self.printBoard()
            #Conditional to check if the game has concluded without a winner
            #This occurs when the board has been filled without a winner (9 total moves)
            if self.numSuccessfulTurns == 9:
                print("It's a tie! The match has concluded")
                return self.printBoard()
            #Prints the board to show where the user entered their symbol
            self.printBoard()
            #Upon successfully placing the turn, update the time that the game was last updated
            self.lastUpdate = datetime.datetime.now()
            #After successful move, change whose turn it is in the game
            if self.playersTurn == self.player1:
                self.playersTurn = self.player2
            else:
                self.playersTurn = self.player1
            return ""
        #If the player attempting to post a turn is out of turn, throw a value error
        elif not (self.playersTurn == player):
            raise ValueError("It is not your turn, please wait to post a move until it is your turn")
        #Conditional that handles the case of the desired spot being filled
        elif not(self.board[move] == ' '):
            raise ValueError('That spot is already filled. Choose a spot to place your symbol')

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
