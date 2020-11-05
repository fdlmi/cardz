from cardz.cardz import *
from flask import Flask, jsonify

app = Flask(__name__)

games = []
decks = []
players = []


# not asked for
@app.route("/games", methods=["GET"])
def games_():
    return jsonify(
        {
            "state": "OK",
            "len": len(games),
            "games": [game.serialize() for game in games],
        }
    )


# not asked for
@app.route("/decks", methods=["GET"])
def decks_():
    return jsonify(
        {
            "state": "OK",
            "len": len(decks),
            "decks": [deck.serialize() for deck in decks],
        }
    )


# not asked for
@app.route("/players", methods=["GET"])
def players_():
    return jsonify(
        {
            "state": "OK",
            "len": len(players),
            "players": [player.serialize() for player in players],
        }
    )


@app.route("/game/create", methods=["POST"])
def game_create():
    id = getNewID(games)
    game = Game(id)
    games.append(game)

    d = {"state": "OK"}
    d.update(game.serialize())
    return jsonify(d)


@app.route("/deck/create", methods=["POST"])
def deck_create():
    id = getNewID(decks)
    deck = Deck(id)
    decks.append(deck)

    d = {"state": "OK"}
    d.update(deck.serialize())
    return jsonify(d)


@app.route("/game/<id>", methods=["DELETE"])
def game_delete(id):
    id = int(id)
    games.remove([game for game in games if game.id == id][0])
    return jsonify(
        {
            "state": "OK",
            "type": "game",
            "id": id,
        }
    )


@app.route("/game/<gameID>/addDeck/<deckID>", methods=["POST"])
def game_addDeck(gameID, deckID):
    # make this a function
    try:
        gameID = int(gameID)
        game = [game for game in games if game.id == gameID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Game not found"})

    try:
        deckID = int(deckID)
        deck = [deck for deck in decks if deck.id == deckID][0]
    except:
        return jsonify({"state": "FAIL", "message": "Deck not found"})

    game.addDeck(deck)

    # FIXME copied from games_
    return jsonify(game.serialize())


@app.route("/game/<gameID>/addPlayer", methods=["POST"])
def game_addPlayer(gameID):
    # make this a function
    try:
        gameID = int(gameID)
        game = [game for game in games if game.id == gameID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Game not found"})

    id = getNewID(players)
    player = Player(id)
    players.append(player)
    game.addPlayer(player)
    return jsonify(game.serialize())


@app.route("/game/<gameID>/removePlayer/<playerID>", methods=["POST"])
def game_removePlayer(gameID, playerID):
    # make this a function
    try:
        gameID = int(gameID)
        game = [game for game in games if game.id == gameID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Game not found"})

    try:
        playerID = int(playerID)
        player = [player for player in players if player.id == playerID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Player not found"})

    game.removePlayer(player)
    return jsonify(game.serialize())


@app.route("/game/<gameID>/shuffleGameDeck", methods=["POST"])
def game_shuffleGameDeck(gameID):
    try:
        gameID = int(gameID)
        game = [game for game in games if game.id == gameID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Game not found"})

    game.shoe.shuffle()
    return jsonify(game.serialize())


@app.route("/game/<gameID>/dealCards/<numCards>/<playerID>", methods=["POST"])
def game_dealCards(gameID, numCards, playerID):
    try:
        gameID = int(gameID)
        game = [game for game in games if game.id == gameID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Game not found"})

    numCards = int(numCards)

    try:
        playerID = int(playerID)
        player = [player for player in players if player.id == playerID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Player not found"})

    game.dealCards(numCards, player)
    return jsonify(player.serialize())


# For listCards
@app.route("/player/<playerID>", methods=["GET"])
def player_(playerID):
    try:
        playerID = int(playerID)
        player = [player for player in players if player.id == playerID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Player not found"})

    return jsonify(player.serialize())


@app.route("/game/<gameID>/playersValue", methods=["GET"])
def game_playersValue(gameID):
    try:
        gameID = int(gameID)
        game = [game for game in games if game.id == gameID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Game not found"})

    return jsonify(
        sorted([
            {
                "id": player.id,
                "type": "player",
                "value": sum([card.value for card in player.cards]),
            }
            for player in game.players
        ], key=lambda player: player["value"], reverse=True)
    )

@app.route("/game/<gameID>/countPerSuit", methods=["GET"])
def game_countPerSuit(gameID):
    try:
        gameID = int(gameID)
        game = [game for game in games if game.id == gameID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Game not found"})

    return jsonify(game.shoe.countPerSuit())

@app.route("/game/<gameID>/countCards", methods=["GET"])
def game_countCards(gameID):
    try:
        gameID = int(gameID)
        game = [game for game in games if game.id == gameID][0]
    except:
        # FIXME return 5xx?
        return jsonify({"state": "FAIL", "message": "Game not found"})

    return jsonify(game.shoe.countCards())


def getNewID(a):
    """
    From list of dict, get a new int for key id
    Return 1 if a is empty
    """
    id = 1
    if len(a) > 0:
        maxID = max([e.id for e in a])
        id = maxID + 1
    return id


if __name__ == "__main__":
    # gameCreate()
    app.run(port=8080)
