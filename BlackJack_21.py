""" BlackJack 
    Place a bet then draw cards against the dealer.
    Closest to 21 wins
    aces count as 11 or 1
"""

import random

suits =('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 
         'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six': 6, 'Seven':7, 'Eight':8, 'Nine':9,
          'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':10}

playing = True

#game classes

class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]

    def __str__ (self):
        return self.rank + ' of ' + self.suit

class Deck:
    
    def __init__(self):       
        self.all_cards = []        
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)
                
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    def deal(self):
        return self.all_cards.pop()

class Hand:
    def __init__(self):
        self.cards = []
        self.value  = 0 
        self.aces = 0
        
    def add_card(self, card):
        #pass card from deck class
        self.cards.append(card)
        self.value += values[card.rank]
        
        #track aces
        if card.rank == 'Ace':
            self.aces += 1
            
    def adjust_for_aces(self):
        
        while self.value > 21 and self.aces > 0:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self):
        self.total = 100  
        self.bet = 0
        
    def win_bet(self):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

#game functions

def take_bet(chips):
    while True:
        
        try:
            chips.bet = int(input("How many chips would you like to bet?"))
        except:
            print("Sorry please choose an interger.")
        else:
            if chips.bet > chips.total:
                print("You dont have enout chips. you have {}".format(chips.total))
            else:
                break

def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_aces()

def hit_or_stand(deck, hand):
    global playing
    
    while True:
        x = input("Hit or stand? Enter h or s")
        
        if x[0].lower() == 'h':
            hit(deck, hand)
            
        elif x[0].lower() == 's':
            print("Player stands dealer turn.")
            playing = False
            
        else:
            print('Sorry I dont understand please enter h or s.')
            continue
        break

def show_some(player, dealer):
    print("\n Dealers Hand:")
    print("First card hidden!")
    print(dealer.cards[1])
    
    print("\n Players cards:")
    for card in player.cards:
        print(card)
    

def show_all(player, dealer):
        
    print("\n Dealer cards:")
    for card in dealer.cards:
        print(card)
    print(f"Value of dealers hand is {dealer.value}")
        
    print("\n Players cards:")
    for card in player.cards:
        print(card)
    print(f"Value of players hand is {player.value}")       

def player_busts(player,dealer,chips):
    print("Player busts!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print("Dealer busts!")
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("Dealer wins!")
    chips.lose_bet()
    
def push(player,dealer):
    print("Dealer and Player tie! It's a push.")

# Game logic
while True:
    #welcome message
    print("Welcome to BlackJack!")
    
    #set up deck
    deck = Deck()
    deck.shuffle()
    
    #set up player and dealer hands
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())
    
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
    #set up player chips
    player_chips = Chips()
    
    #take a bet
    take_bet(player_chips)
    
    #show cards for start of game
    show_some(player_hand, dealer_hand)
    
    while playing:
        #prompt for hit or stand
        hit_or_stand(deck, player_hand)
        
        #show cards again
        show_some(player_hand, dealer_hand)
        
        # if player's hand exceeds 21, run player_busts() and breakloop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)
            
            break
            
    #dealer plays until 17
    if player_hand.value <= 21:
        
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)
            
        show_all(player_hand, dealer_hand)
        
         #check for win cases
        if dealer_hand.value > 21:
            dealer_busts(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)

        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)

        else:
            push(player_hand,dealer_hand) 
        
    #update chip count
    print("\n Players chips are: {}".format(player_chips.total))
    
    #promt for play again
    new_game = input('Would you like to play another hand? y/n')
    
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('thanks for playing. Goodbye.')
        break