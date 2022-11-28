from typing import List, Tuple
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

def shuffle_deck(deck: List[str]) -> List[str]:
    return random.sample(deck, k=len(deck))

def deal(deck: List[Tuple[str,str]]) -> Tuple[List[Tuple[str,str]], List[Tuple[str,str]]]:
        return ([deck[0],deck[2]],[deck[1],deck[3]])

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

def hand_string(hand: List[Tuple[str,str]]) -> str:
    return ",".join(["".join(card) for card in hand])

def print_hand_status(dealer: List[Tuple[str,str]], player: List[Tuple[str,str]]) -> None:
    '''
    print current hand status of dealer and player
    '''
    #TODO: obscure dealer's second card until stand
    print(f'Dealer: {hand_string(dealer)} worth: {value_of_hand(dealer)}\n')
    print(f'Player: {hand_string(player)} worth: {value_of_hand(player)}\n')
 
    return None

#TODO: do I need this?
def value_of_ace(cards: List[str]) -> int:
    '''
    calculate the most advantegous value for an ace card
    if an ace is already in hand, count it as 11 points.
    '''
    tot = sum([value_of_card(card) for card in cards])
    if 'A' in cards and tot + 10 < 21:
        tot += 10
    if 11 + tot > 21:
        return 1
    else:
        return 11

#Higher payout for nat blackjack: usually 2:1 or 3:2 - NATURAL_PAYOUT
def is_natural_blackjack(card_one: str, card_two: str) -> bool:
    '''
    return if you were dealt a natural blackack where
    one card is worth 10 points and the other is an ace
    '''
    return any((x in {'J','Q','K','10'} and y in {'A'} for x,y in [(card_one, card_two),(card_two, card_one)]))

def can_split_pairs(hand: List[Touple[str,str]]) -> bool:
    '''
    a player can split pairs if the card values are equal.
    these are then treated as two seperate hands
    '''
    if len(hand) > 2:
        return False
    return value_of_card(card_one) == value_of_card(card_two)

def can_double_down(card_one: str, card_two: str) -> bool:
    '''
    when the original two cards dealt total 9,10, or 11 points,
    a player can place an additional bet equal to their original bet.
    '''
    return value_of_card(card_one) + value_of_card(card_two) in {9,10,11}

def can_hit_again(hand: List[Tuple[str,str]]) -> bool:
    '''
    if value is under 21, player can hit again
    '''
    return value_of_hand(cards) < 21
