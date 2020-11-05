#!/bin/sh

# Create a game and a deck
curl -s -X POST localhost:8080/game/create | jq
curl -s -X POST localhost:8080/deck/create | jq

# Add the deck to the game
curl -s -X POST localhost:8080/game/1/addDeck/1 | jq
curl -s -X POST localhost:8080/game/1/shuffleGameDeck | jq

# Add 2 players to the game
curl -s -X POST localhost:8080/game/1/addPlayer | jq
curl -s -X POST localhost:8080/game/1/addPlayer | jq

# Deal cards to players
curl -s -X POST localhost:8080/game/1/dealCards/1/1 | jq
curl -s -X POST localhost:8080/game/1/dealCards/1/2 | jq
curl -s -X POST localhost:8080/game/1/dealCards/2/2 | jq
