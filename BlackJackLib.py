from typing import List, Tuple, Optional
from enum import Enum
from copy import deepcopy
import random
import sys

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
        return color_card(hand[0]) + ",XX"
    return ",".join([color_card(card) for card in hand])

def print_hand_status(
        dealer: List[Tuple[str,str]],
        player: List[Tuple[str,str]],
        player2: List[Tuple[str,str]] = None,
        dealer_hidden = True) -> None:
    '''
    print current hand status of dealer and player
    '''
    if dealer_hidden:
        print_color(f"\tDealer: {hand_string(dealer, dealer_hidden)} worth: Unknown\n","gold")
    else:
        print_color(f"\tDealer: {hand_string(dealer, dealer_hidden)} worth: {value_of_hand(dealer)}\n","gold")
    print_color(f"\tPlayer: {hand_string(player)} worth: {value_of_hand(player)}","blue")
    if player2 is not None:
        print_color(f"\tPlayer: {hand_string(player2)} worth: {value_of_hand(player2)}","blue")

    print("\n") 
    return None

def color_card(card: Tuple[str,str]) -> str:
    if card[1] in ['♦','♥']:
        return f'\033[31;107m{card[0]}{card[1]}\033[0m'
    else:
        return f'\033[30;107m{card[0]}{card[1]}\033[0m'
    return 'poop'

def print_color(text: str,color = '37m') -> None:
    TC = {
            'red':'31m',
            'green':'32m',
            'gold':'33m',
            'blue':'34m',
            'magenta':'35m',
            'cyan':'36m',
            'bred':'91m',
            'bgreen':'92m',
            'byellow':'93m',
            'bblue':'94m',
            'bmagenta':'95m',
            'bcyan':'96m',
            'bwhite':'97m'
            }
    if color not in TC.keys():
        print(text)
    else:
        print(f"\033[{TC[color]}{text}\033[0m")
    return None

'''
Options for Player
'''

def accept_bet(
        prompt: str,
        max_bet,
        retries = 4,
        reminder = "    Please try again. ",
        min_bet = MINBET
        ) -> int:

    while True:
        bet = str(input(prompt))
        if bet.isdecimal():
            if min_bet <= int(bet) and int(bet) <= max_bet:
                return int(bet)
            elif int(bet) < min_bet:
                print_color("\n    The Dealer says 'That's not enough for me to throw down some cards.'","gold")
            elif int(bet) > max_bet:
                print_color("\n    Your ego's writing checks your wallet can't cash.")
        elif retries == 0:
            print_color("    The Dealer shakes their head. You're playing the fool.","gold")
        else:
            print_color("\n    The Dealer gives you the side eye. 'We don't accept that here. Whole Dollar amounts only.'","gold")
        retries -= 1
        if retries < 0:
            print_color("    The Bouncer approaches. It's time to go.\n","cyan")
            sys.exit()
        print_color(reminder+f"{retries+1} retries remain before the Bouncer kicks your @** out.\n","cyan")
    return False

def ask_ok(
        prompt: str,
        retries = 4,
        reminder = "\n    The Dealer looks at you. 'Sorry, I didn't understand that.'",
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
            print_color("    The Bouncer approaches. It's time to go.\n","cyan")
            sys.exit()

        print_color(reminder,"gold")
        if retries <= 3:
            print_color(f"    {retries+1} retries remain before the Bouncer kicks your @** out.\n")
    return False

def is_natural_blackjack(hand: List[Tuple[str,str]]) -> bool:
    '''
    return if you were dealt a natural blackjack where
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
            print("\n")
            print_hand_status(dealer, player)
        else:
            break

    if value_of_hand(player) == 21:
        print_color("    WHOOHOOO! 21! Let's see what the Dealer has.\n","green")
    return player, deck

def split(
        player: List[Tuple[str,str]],
        deck: List[Tuple[str,str]]) -> Tuple[List[Tuple[str,str]]]:
    '''
    create two hands out of one hand. Each will play as seperate hands:
    returns player, player2, deck
    '''
    return ([player[0], deck[0]],[player[1], deck[1]], deck[2:])

'''
Dealer and Player Turns
'''

def dealer_turn(
        dealer: List[Tuple[str,str]],
        deck: List[Tuple[str,str]]) -> Tuple[List[Tuple[str,str]]]:
    '''
    The Dealer's turn is simple: if their hand is under 17, hit.
    if they have a soft 17 (an ace in the hand worth 11), hit.
    '''

    print_color(f"\tDealer: {hand_string(dealer)} worth: {value_of_hand(dealer)}\n","gold")

    while value_of_hand(dealer) < 17:
        print_color("\tThe Dealer takes a card\n")
        dealer, deck = hit(dealer, deck)
        print_color(f"\tDealer: {hand_string(dealer)} worth: {value_of_hand(dealer)}\n","gold")

    #if the dealer has a soft 17, continue to take more cards.
    if value_of_hand(dealer) == 17 and sum([value_of_card(x) for x,y in dealer]) != 17:
        dealer, deck = hit(dealer, deck)
        dealer, deck = dealer_turn(dealer, deck)
    print_color(f'''    The Dealer is done with their turn. You both look at your cards.
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
        print_color(f"\tPlayer: {hand_string(player)} worth: {value_of_hand(player)}\n","blue")
        return player, deck, player2

    if sp:
        #the player chose to split their hand and they will play as two seperate hands
       player, player2, deck = split(player, deck)
       print_color(f"""
    You now have two hands:
        \033[34mHand1 {hand_string(player)} worth: {value_of_hand(player)}
        Hand2 {hand_string(player2)} worth: {value_of_hand(player2)}\033[0m

    \033[34mPlaying Hand1: {hand_string(player)} worth: {value_of_hand(player)}\033[0m""")

    player, deck = player_hit(player,dealer,deck)

    if player2 is not None:
        print_color(f"\n    Playing Hand2: {hand_string(player2)} worth: {value_of_hand(player2)}",'blue')
        player2, deck = player_hit(player2,dealer,deck)

    return player, deck, player2
