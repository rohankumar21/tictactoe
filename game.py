from flask import Flask, render_template, jsonify, request
from tictactoe import game, player
import uuid, datetime, atexit, time
from apscheduler.schedulers.background import BackgroundScheduler

app = Flask(__name__)
#Hashmap for games that are currently active on the server
server = {}

@app.route('/')
def home():
    return """
        <html><body>
            <h2>Welcome to TicTacToe</h2>
        </body></html>
        """

#App route for creating a new game
@app.route('/createGame', methods=['POST'])
def createGame():
    #Query parameter for desired name for player 1
    player1Name = request.args['player1Name']
    #Conditional that sets default name for player 1
    if player1Name == '':
        player1Name = 'Player 1'
    #Query parameter for desired symbol for player 1
    player1Symbol = request.args['player1Symbol']
    #Conditional that sets default symbol for player 1
    if player1Symbol == '':
        player1Symbol = 'X'
    #Query parameter for desired name for player 2
    player2Name = request.args['player2Name']
    #Conditional that sets default name for player 2
    if player2Name == '':
        player2Name = 'Player 2'
    #Query parameter for desired symbol for player 2
    player2Symbol = request.args['player2Symbol']
    #Conditional that sets default symbol for player 2
    if player2Symbol == '':
        player2Symbol = 'O'
    #Instantiate player objects for player 1 and player 2 based on query parameters passed in
    player1 = player(player1Name, player1Symbol)
    player2 = player(player2Name, player2Symbol)
    #Instantiation of a new game object
    newGame = game()
    #Setting player 1 and player 2 variables for the new game
    newGame.player1 = player1
    newGame.player2 = player2
    #Sets current players turn to player 1 for the current game
    newGame.playersTurn = player1
    #Creates a unique 4 digit game ID for the current ID based on a hash of the players information in the game
    gameID = abs(hash(player1Name+player2Name+player1Symbol+player2Symbol)) % (10 ** 4)
    #Confirms that the game ID created is not present in the server
    if(not gameID in server.keys()):
        server[gameID] = newGame
    #Adds a game value to the server map with a gameID key
    server[gameID] = newGame
    #Creates a unique 4 digit authorization token for the game
    #Used to ensure that only the players in the game can alter the board and post turns
    newGame.authToken = str(uuid.uuid4())[:4]
    #Print the empty board once the game has been successfully created
    newGame.printBlankBoard()
    #Updates the time that the game was last played (used to ensure that idle games don't take up space in the server)
    newGame.lastUpdate = datetime.datetime.now()
    #Returns a jsonify of prevalent game information
    return jsonify(gameID = gameID, authToken = newGame.authToken, lastUpdate = newGame.lastUpdate)

#Return board state (players, symbols, and board state in jsonify)
@app.route('/getGame', methods=['GET'])
def getGame():
    #Query parameter of lookupID for desired game to access from the server
    lookupID = request.args['lookupID']
    #If valid lookupID entered, return a jsonify of the desired game's information
    if(int(lookupID) in server.keys()):
        retrievedGame = server[int(lookupID)]
        return jsonify(player1Name = retrievedGame.player1.name, player1Symbol = retrievedGame.player1.symbol, player2Name = retrievedGame.player2.name, player2Symbol = retrievedGame.player2.symbol, gameState = retrievedGame.getGameState())
    #If incorrect lookupID is provided, return a KeyError
    else:
        raise KeyError('Invalid game ID entered')

#App route that allows players to post turns to their corresponding game
@app.route('/postTurn', methods=['POST'])
def postTurn():
    #Query parameter that requires the gameID of the desired game to edit
    gameID = request.args['gameID']
    #Query parameter for authorization token to ensure the proper players are
    #editing the game
    authToken = request.args['authToken']
    #Query parameter for the desired players turn
    playerName = request.args['playerName']
    #Query parameter for the desired players placement on the board
    playerMove = request.args['playerMove']
    #Accesses the game from the server based on the gameID query parameter
    retrievedGame = server[int(gameID)]
    #Conditional to check that the current player attempting to post a turn
    #is doing so within the parameters of their own game
    if(retrievedGame and (retrievedGame.player1.name == playerName or
       retrievedGame.player2.name == playerName) and
       retrievedGame.authToken == authToken):
        #Conditional to see if the current game has been won by one of the players or if a tie has occurred
        if(retrievedGame.checkWin(retrievedGame.player1) or retrievedGame.checkWin(retrievedGame.player2) or retrievedGame.numSuccessfulTurns >= 9):
            return "Game has concluded"
        #If the match hasn't concluded, post the turn to the corresponding game
        else:
            #Post the desired turn to the corresponding game after finding the player for the game based on the player name query parameter
            retrievedGame.turn(retrievedGame.findPlayer(playerName), int(playerMove))
            return jsonify(playersName = playerName, successfulMove = playerMove, gameState = retrievedGame.getGameState())
    #If any parameters provided were incorrect, raise a KeyError
    else:
        raise KeyError('Unable to update game')

#Error handler for ValueError's
@app.errorhandler(ValueError)
def handle_value_error(e):
    return str(e), 500

#Error handler for KeyError's
@app.errorhandler(KeyError)
def handle_value_error(e):
    return str(e), 500

#Function that removes a game from the server if the game hasn't been updated
#within 5 minutes
def removeAfterTime(server):
    for k in list(server):
        currentGame = server[k]
        currentTime = datetime.datetime.now()
        if(float((currentTime - currentGame.lastUpdate).total_seconds())/60 >= 5):
            del server[k]
            print("Game has been terminated due to inactivity")

#apscheduler that runs the removeAfterTime function every 30 seconds
scheduler = BackgroundScheduler()
#Adds the removeAfterTime function as a job to the background scheduler
scheduler.add_job(removeAfterTime, "interval", [server], seconds = 30)
scheduler.start()
#Shuts down the apscheduler upon closing the flask app
atexit.register(lambda: scheduler.shutdown())

# Launch the FlaskPy dev server
app.run(host="localhost", debug=True)
