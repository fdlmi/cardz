# Cardz

A Basic Deck of Cards Game -- LogMeIn assignement

Because we pretend this will become a part of a new product, I chose to serve this API over HTTP for ease
of integration with other unknown parts of the product.

Because this is for a DevOps position, I made sure the application was easily deployable in
a production environment.

Data persistence wasn't mentionned, so I kept it simple and the data only resides in memory.
It would be trivial to put the data into a database.

The try/excpet blocks are repeated too much to my liking but I unfortunately did not have the time
to fix this, although it shouldn't be too hard.

The resulting docker image is 55MB.

## Developer Installation

### Clone repo and create a virtual environment
```bash
  $ git clone https://github.com/fdlmi/cardz.git
  $ cd cardz
  $ mkvirtualenv cardz
  $ pip install -e ".[dev]"
```

### Launch Cardz Locally
#### Development mode
```bash
  (cardz) $ FLASK_ENV=development python cardz_api.py
```
#### Production mode
```bash
  (cardz) $ gunicorn cardz_api:app -b:8080 -w${nworkers}
```

### Testing
Simple test script
```bash
$ ./test.sh
```

## Production Installation

### Use docker image
#### Build
```bash
  $ git clone https://github.com/fdlmi/cardz.git
  $ cd cardz
  $ docker build -t cardz .
```
#### Run
```bash
  $ docker run -p8080:8080 cardz
```

## Usage
The following examples are using `curl` for simplicity. It can be piped to `jq` for nicer output.

### Create a game `POST /game/create`
```bash
$ curl -s -X POST localhost:8080/game/create
```
```json
{
  "id": 1,
  "state": "OK",
  "type": "game"
}
```

### Delete a game `DELETE /game/<id>`
```bash
$ curl -s -X DELETE localhost:8080/game/1
```
```json
{
  "id": "1",
  "state": "OK",
  "type": "game"
}
```

### Create a deck `POST /deck/create`
```bash
$ curl -s -X POST localhost:8080/deck/create
```
```json
{
  "id": 1,
  "state": "OK",
  "type": "deck"
}
```

### Add a deck to a game deck `POST /game/<gameID>/addDeck/<deckID>`
```bash
$ curl -s -X POST localhost:8080/game/1/addDeck/1
```
```json
{
  "id": 1,
  "players": [],
  "type": "game"
}
```

### Add player to a game `POST /game/<gameID>/addPlayer`
```bash
$ curl -s -X POST localhost:8080/game/1/addPlayer
```
```json
{
  "id": 1,
  "players": [
    {
      "cards": [],
      "id": 1,
      "type": "player"
    }
  ],
  "type": "game"
}
```

### Remove players from a game `POST /game/<gameID>/removePlayer/<playerID>`
```bash
$ curl -s -X POST localhost:8080/game/1/removePlayer/1
```
```json
{
  "id": 1,
  "players": [],
  "type": "game"
}
```

### Deal cards to a player in a game from the game deck `POST /game/<gameID>/dealCards/<numCards>/<playerID>`
```bash
$ curl -s -X POST localhost:8080/game/1/dealCards/1/1
```
```json
{
  "cards": [
    {
      "face": 1,
      "suit": "diamonds",
      "type": "card",
      "value": 1
    }
  ],
  "id": 1
}
```

### Get the list of cards for a player `GET /player/<playerID>`
```bash
curl -s -X GET localhost:8080/player/1 | jq ".cards"
```
```json
[
  {
    "face": "King",
    "suit": "spades",
    "type": "card",
    "value": 13
  },
  {
    "face": 6,
    "suit": "spades",
    "type": "card",
    "value": 6
  }
]
```

### Get the list of players in a game along with the total added value of all the cards each player holds, descending order of value `GET /game/<gameID>/playersValue`
```bash
curl -s -X GET localhost:8080/game/1/playersValue
```
```json
[
  {
    "id": 1,
    "type": "player",
    "value": 23
  },
  {
    "id": 2,
    "type": "player",
    "value": 0
  }
]
```

### Get the count of how many cards per suit are left undealt in the game deck `GET /game/<gameID>/countPerSuit`
```bash
$ curl -s -X GET localhost:8080/game/1/countPerSuit
```
```json
{
  "clubs": 5,
  "diamonds": 9,
  "hearts": 15,
  "spades": 13
}
```

### Get the count of each card remaining in the game deck sorted by suit and face value `GET /game/<gameID>/countCards`
```bash
curl -s -X GET localhost:8080/game/1/countCards
```
```json
[
  {
    "count": 1,
    "suit": "hearts",
    "value": 13
  },
  {
    "count": 2,
    "suit": "spades",
    "value": 3
  },
  {
    "count": 1,
    "suit": "diamonds",
    "value": 1
  }
]
```


### Shuffle the game deck (shoe) `POST /game/<gameID>/shuffleGameDeck`
```bash
$ curl -s -X POST localhost:8080/game/1/shuffleGameDeck
```
```json
{
  "id": 1,
  "players": [],
  "type": "game"
}
```
