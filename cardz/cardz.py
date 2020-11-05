#!/usr/bin/env python

import random


class Game:
    def __init__(self, id):
        self.id = id
        self.players = []
        self.shoe = Shoe()

    def serialize(self):
        return {
            "id": self.id,
            "type": "game",
            "players": [player.serialize() for player in self.players],
        }

    def addDecks(self, nDecks):
        for i in range(0, nDecks):
            self.shoe.addDeck(Deck())

    def addDeck(self, deck):
        self.shoe.addDeck(deck)

    def addPlayer(self, player):
        self.players.append(player)

    def removePlayer(self, player):
        self.players.remove(player)

    def dealCards(self, numberOfCards, player):
        """
        Give numberOfCards cards to player player
        FIXME what if no cards left?
        """
        for i in range(0, numberOfCards):
            player.cards.append(self.shoe.cards.pop())

    def listCards(self):
        self.shoe.listCards()


class Deck:
    def __init__(self, id):
        self.id = id
        """
        Fifty-two playing cards in four suits:
        hearts, spades, clubs, and diamonds, with face values of Ace, 2-10, Jack, Queen, and King.
        """
        self.cards = []
        for suit in ["hearts", "spades", "clubs", "diamonds"]:
            for value in range(13, 0, -1):
                self.cards.append(Card(suit, value))

    def serialize(self):
        return {
            "id": self.id,
            "type": "deck",
            "nCards": len(self.cards),
        }

    def cards(self):
        return self.cards


class Card:
    def __init__(self, suit, value):
        self.suit = suit
        self.value = value

    def serialize(self):
        return {
            "type": "card",
            "suit": self.suit,
            "value": self.value,
            "face": self.face(),
        }

    def face(self):
        if self.value == 1:
            return "Ace"
        elif self.value == 11:
            return "Jack"
        elif self.value == 12:
            return "Queen"
        elif self.value == 13:
            return "King"
        else:
            return self.value


class Shoe:
    """
    A Shoe is a game deck in which one or more decks are added.
    """
    def __init__(self):
        self.cards = []

    def addDeck(self, deck):
        self.cards.extend(deck.cards)

    def shuffle(self):
        """
        Shuffle returns no value, but results in the cards in the game deck being randomly permuted.
        """
        # Using Fisher-Yates because random.shuffle() is prohibited but RNG is fine
        for i in range(len(self.cards) - 1, 0, -1):
            j = random.randint(0, i + 1)
            self.cards[i], self.cards[j] = self.cards[j], self.cards[i]

    def countPerSuit(self):
        """
        Count of how many cards per suit are left undealt in the game deck (example: 5 hearts, 3 spades, etc.)
        """
        nHearts = len([card for card in self.cards if card.suit == "hearts"])
        nSpades = len([card for card in self.cards if card.suit == "spades"])
        nClubs = len([card for card in self.cards if card.suit == "clubs"])
        nDiamonds = len([card for card in self.cards if card.suit == "diamonds"])
        return {
            "hearts": nHearts,
            "spades": nSpades,
            "clubs": nClubs,
            "diamonds": nDiamonds,
        }

    def countCards(self):
        """
        Get the count of each card (suit and value) remaining in the game deck sorted by
        suit ( hearts, spades, clubs, and diamonds) and face value from high value to
        low value (King, Queen, Jack, 10?.2, Ace with value of 1)
        """
        l = []
        for suit in ["hearts", "spades", "clubs", "diamonds"]:
            for value in range(13, 0, -1):
                n = len(
                    [
                        card
                        for card in self.cards
                        if card.suit == suit and card.value == value
                    ]
                )
                if n > 0:
                    l.append(
                        {
                            "count": n,
                            "suit": suit,
                            "value": value,
                        }
                    )
        return l


class Player:
    def __init__(self, id):
        self.id = id
        self.cards = []

    def serialize(self):
        return {
            "id": self.id,
            "type": "player",
            "cards": [card.serialize() for card in self.cards],
        }
