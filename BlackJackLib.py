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
BlackJack 'Pretty Print' light
'''

def hand_string(hand: List[Tuple[str,str]], second_hidden = False) -> str:
    if second_hidden:
        return "".join(hand[0]) + ", XX"
    return ",".join(["".join(card) for card in hand])

def print_hand_status(
        dealer: List[Tuple[str,str]],
        player: List[Tuple[str,str]],
        dealer_hidden = True) -> None:
    '''
    print current hand status of dealer and player
    '''
    #TODO: obscure dealer's second card until stand
    if dealer_hidden:
        print(f'Dealer: {hand_string(dealer, dealer_hidden)} worth: Unknown')
    else:
        print(f'Dealer: {hand_string(dealer, dealer_hidden)} worth: {value_of_hand(dealer)}\n')
    print(f'Player: {hand_string(player)} worth: {value_of_hand(player)}\n')
 
    return None

'''
Options for Player
'''

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

def dealer_turn(
        dealer: List[Tuple[str,str]],
        deck: List[Tuple[str,str]]) -> Tuple[List[Tuple[str,str]]]:
    '''
    The dealer's turn is simple: if their hand is under 17, hit.
    '''

    print(f'''
    The dealer takes their turn.
    They turn over their hidden card.
        \n\n''')
    #print(f'Dealer: {hand_string(dealer)} worth: {value_of_hand(dealer)}\n')

    while value_of_hand(dealer) < 17:
        print(f'Dealer: {hand_string(dealer)} worth: {value_of_hand(dealer)}\n')
        print('The Dealer takes a card')
        dealer, deck = hit(dealer, deck)
    return dealer, deck


