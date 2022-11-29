from typing import List, Tuple, Optional
from enum import Enum
from copy import deepcopy
import random

'''
french-suited playing card suits
'''
SUITS = ['♦','♣','♥','♠']
CARDVALUES = ['A','K','Q','J','10','9','8','7','6','5','4','3','2']

DECK = [(y,x) for x in SUITS for y in CARDVALUES] #52 cards

NATURAL_PAYOUT = 1.5
INITIALMONEY = 500
MINBET = 50
WIN = 50000

'''
Round Setup
'''

def shuffle_deck(deck: List[str]) -> List[str]:
    return random.sample(deck, k=len(deck))

def deal(deck: List[Tuple[str,str]]) -> Tuple[List[Tuple[str,str]], List[Tuple[str,str]]]:
        return ([deck[0],deck[2]],[deck[1],deck[3]])
'''
Math Functions
'''

def value_of_card(card: str) -> int:
    '''
    return the value of a card
    '''
    if card in {'J','Q','K'}:
        return 10
    if card in {'A'}:
        return 1
    else:
        return int(card)

def value_of_hand(hand: List[Tuple[str,str]]) -> int:
    tot =  sum([value_of_card(x) for x,y in hand])
    if 'A' in [x for x,y in hand] and tot + 10 <= 21:
        tot += 10
    return tot

def player_win(player: List[Tuple[str,str]], dealer: List[Tuple[str,str]]) -> Optional[bool]:
    if value_of_hand(player) == value_of_hand(dealer):
        return None
    return value_of_hand(player) > value_of_hand(dealer)

'''
BlackJack 'Pretty Print' functions
'''

def hand_string(hand: List[Tuple[str,str]], second_hidden = False) -> str:
    if second_hidden:
        return "".join(hand[0]) + ", XX"
    return ",".join(["".join(card) for card in hand])

def print_hand_status(
        dealer: List[Tuple[str,str]],
        player: List[Tuple[str,str]],
        player2: List[Tuple[str,str]] = None,
        dealer_hidden = True) -> None:
    '''
    print current hand status of dealer and player
    '''
    if dealer_hidden:
        print(f"\tDealer: {hand_string(dealer, dealer_hidden)} worth: Unknown")
    else:
        print(f"\tDealer: {hand_string(dealer, dealer_hidden)} worth: {value_of_hand(dealer)}\n")
    print(f"\tPlayer: {hand_string(player)} worth: {value_of_hand(player)}")
    if player2 is not None:
        print(f"\tPlayer: {hand_string(player2)} worth: {value_of_hand(player2)}")

    print("\n") 
    return None

'''
Options for Player
'''

def accept_bet(
        prompt: str,
        max_bet,
        retries = 4,
        reminder = "    The Dealer gives you the side eye. 'We don't accept that here.'",
        min_bet = MINBET
        ) -> int:

    while True:
        bet = str(input(prompt))
        if bet.isdigit() and min_bet <= int(bet) and int(bet) <= max_bet:
            return int(bet)
        retries -= 1
        if retries < 0:
            raise ValueError("invalid user response")
        print(reminder)
    return False

def ask_ok(
        prompt: str,
        retries = 4,
        reminder = "Sorry, I didn't understand. Please enter again - Y/N: ",
        yes = {'y','ye','yes'},
        no = {'n','no','nop','nope','nada'})-> bool:

    while True:
        ok = str(input(prompt)).lower()
        if ok in yes:
            return True
        if ok in no:
            return False
        retries -= 1
        if retries < 0:
            raise ValueError("invalid user response")
        print(reminder)
    return False

def is_natural_blackjack(hand: List[Tuple[str,str]]) -> bool:
    '''
    return if you were dealt a natural blackack where
    one card is worth 10 points and the other is an ace
    payout for nat blackjack is usually 2:1 or 3:2. Value is NATURAL_PAYOUT
    '''
    if len(hand) >2:
        return False
    return value_of_hand(hand) == 21 

def can_split_pairs(hand: List[Tuple[str,str]]) -> bool:
    '''
    a player can split pairs if the card values are equal.
    these are then treated as two seperate hands
    '''
    if len(hand) > 2:
        return False
    return value_of_card(hand[0][0]) == value_of_card(hand[1][0])

def can_double_down(hand: List[Tuple[str,str]]) -> bool:
    '''
    when the original two cards dealt total 9,10, or 11 points,
    a player can place an additional bet equal to their original bet.
    '''
    if len(hand) > 2:
        return False
    return value_of_card(hand[0][0]) + value_of_card(hand[1][0]) in {9,10,11}

def can_hit_again(hand: List[Tuple[str,str]]) -> bool:
    '''
    if value is under 21, player can hit again
    '''
    return value_of_hand(cards) < 21

'''
Round Actions
'''

def hit(
        player: List[Tuple[str,str]],
        deck: List[Tuple[str,str]]) -> Tuple[List[Tuple[str,str]]]:
    '''
    add a card from the deck
    '''
    return player + [deck[0]], deck[1:]

def player_hit(
        player: List[Tuple[str,str]],
        dealer: List[Tuple[str,str]],
        deck: List[Tuple[str,str]]) -> Tuple[List[Tuple[str,str]]]:
    '''
    ask the player if they wish to hit, then hit if true
    returns player and dealer
    '''

    while value_of_hand(player) < 21:
        if ask_ok(f"    Would you like to hit or stay? H/S: ",
                yes = {'y','ye','yes', 'h','hit'},
                no =  {'n','no','nop','nope','nada','s','stay'}):
            player, deck = hit(player, deck)
            #print(player)
            print("\n")
            print_hand_status(dealer, player)
        else:
            break

    return player, deck

def split(
        player: List[Tuple[str,str]],
        deck: List[Tuple[str,str]]) -> Tuple[List[Tuple[str,str]]]:
    '''
    create two hands out of one hand. Each will play as seperate hands:
    returns player, player2, deck
    '''
    return ([player[0], deck[0]],[player[1], deck[1]], deck[2:])

def dealer_turn(
        dealer: List[Tuple[str,str]],
        deck: List[Tuple[str,str]]) -> Tuple[List[Tuple[str,str]]]:
    '''
    The Dealer's turn is simple: if their hand is under 17, hit.
    if they have a soft 17 (an ace in the hand worth 11), hit.
    '''

    print(f"\tDealer: {hand_string(dealer)} worth: {value_of_hand(dealer)}\n")

    while value_of_hand(dealer) < 17:
        print("\tThe Dealer takes a card\n")
        dealer, deck = hit(dealer, deck)
        print(f"\tDealer: {hand_string(dealer)} worth: {value_of_hand(dealer)}\n")

    #if the dealer has a soft 17, continue to take more cards.
    if value_of_hand(dealer) == 17 and sum([value_of_card(x) for x,y in dealer]) != 17:
        dealer, deck = hit(dealer, deck)
        dealer, deck = dealer_turn(dealer, deck)
    print(f'''    The Dealer is done with their turn. You both look at your cards.
    ---------------------------------------------------------------------------
    ''')

    return dealer, deck

def player_turn(
        player: List[Tuple[str,str]],
        dealer: List[Tuple[str,str]],
        deck: List[Tuple[str,str]],
        dd = False,
        sp = False
        ) -> Tuple[List[Optional[Tuple[str,str]]]]:
    '''
    the player's turn has several options: they may be able to split OR doubledown
    this function returns player, deck, player2 (if doubledown was chosen)
    '''

    player2 = None

    if dd:
        #the player chose to double down and only recieves one more card
        player, deck = hit(player,deck)
        print(f"\tPlayer: {hand_string(player)} worth: {value_of_hand(player)}\n")
        return player, deck, player2

    if sp:
        #the player chose to split their hand and they will play as two seperate hands
       player, player2, deck = split(player, deck)
       print(f"""
    You now have two hands:
        Hand1 {hand_string(player)} worth: {value_of_hand(player)}
        Hand2 {hand_string(player2)} worth: {value_of_hand(player2)}

    Playing Hand1:""")

    player, deck = player_hit(player,dealer,deck)

    if player2 is not None:
        print("""
    Playing Hand2:""")
        player2, deck = player_hit(player2,dealer,deck)

    return player, deck, player2
