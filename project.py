# Christopher Scott #26419604
# CS 383 Artificial Intelligence
# Final Project - Blackjack Agent

import random

# initialize global variables
in_play = False
message = ""
outcome = ""
score = 0
handsWon = 0
popped = []
player = []
dealer = []
deck = []

# define globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}

# Card class. Hand class calls this draw method for rendering card images onto canvas
class Card:
    def __init__(self, suit, rank):
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None

    def __str__(self):
        return self.rank + self.suit

    def get_suit(self):
        return self.suit

    def get_rank(self):
        return self.rank
        
# Hand class used for adding card objects from Deck() and for getting the value of hands
class Hand:
    def __init__(self):
        self.player_hand = []

    def __str__(self):
        s = ''
        for c in self.player_hand:
            s = s + str(c) + ' '
        return s

    def add_card(self, card):
        self.player_hand.append(card)
        return self.player_hand

    def get_value(self):
        value = 0
        for card in self.player_hand:
            rank = card.get_rank()
            value = value + VALUES[rank]
        for card in self.player_hand:
            rank = card.get_rank()    
            if rank == 'A' and value <= 11:
                value += 10
        return value
        
# Deck class used for re-shuffling between hands and giving card objects to Hand as called
class Deck:
    def __init__(self):
        popped = []
        self.cards = [Card(suit, rank) for suit in SUITS for rank in RANKS]
        self.shuffle()
        
    def __str__(self):
        s = ''
        for c in self.cards:
            s = s + str(c) + ' '
        return s

    def shuffle(self):
        random.shuffle(self.cards)

    def deal_card(self):
        popped = self.cards.pop(0)
        return popped
    
def deal():
    # deal function deals initial hands and adjusts message.
    global in_play, player, dealer, deck, message, score, outcome
    if in_play == True:
        # if player clicks Deal button during a hand, player loses hand in progress
        message = "Here is the new hand"
        score -= 1
        deck = Deck()
        player = Hand()
        dealer = Hand()
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
    if in_play == False:
        # starts a new hand
        deck = Deck()
        player = Hand()
        dealer = Hand()
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        player.add_card(deck.deal_card())
        dealer.add_card(deck.deal_card())
        message = "Here is the new hand."
        # print message
        # print "Dealer: %s= %s" % (dealer, dealer.get_value())
        # print "Player: %s= %s" % (player, player.get_value())
    in_play = True
    outcome = ""

def hit():
    # deals player a new hand and ends hand if it causes a bust.
    global in_play, score, message
    if in_play == True:
        player.add_card(deck.deal_card())
        message = "Hit or Stand?"
        if player.get_value() > 21:
            in_play = False
            message = "Player busted! You Lose! Play again?"
            # score -= 1
            outcome = "Dealer: " + str(dealer.get_value()) + "  Player: " + str(player.get_value())
            # print "Outcome: " + outcome

def stand():
    # hits dealer until >=17 or busts. Determines winner of hand and adjusts score, game state, and messages
    global in_play, score, message, outcome, handsWon
    if in_play == False:
        message = "The hand is already over. Deal again."
        print message
    else:
        while dealer.get_value() < 17:
            dealer.add_card(deck.deal_card())
        if dealer.get_value() > 21:
            message = "Dealer busted. You win! Play again?"
            score += 1
            handsWon += 1
            in_play = False
            
        elif dealer.get_value() > player.get_value():
            message = "Dealer wins! Play again?"
            score -= 1
            in_play = False
        
        elif dealer.get_value() == player.get_value():
            message = "Tie! Dealer wins! Play again?"
            score -= 1
            in_play = False
        
        elif dealer.get_value() < player.get_value():
            message = "You win! Play again?"
            score += 1
            handsWon += 1
            in_play = False
            
        outcome = "Dealer: " + str(dealer.get_value()) + "  Player: " + str(player.get_value())
        # print outcome
        

#Agent Below

threshold = 14
for hands in range(1000000):
    deal()
    while in_play:
        if player.get_value()<threshold:
            hit()
        else:
            stand()
            # outcome = "Dealer: " + str(dealer.get_value()) + "  Player: " + str(player.get_value())
            # print "Outcome: " + outcome
    
    # if (player.get_value() > 21) or (dealer.get_value()>21):
    #     threshold -= 1.0/(hands+1)
    # if (dealer.get_value() > player.get_value()) and(dealer.get_value()<=21):
    #     threshold += 1.0/(hands+1)

    
# print threshold

print handsWon