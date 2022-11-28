import sys
from BlackJackLib import *
import argparse

INITIALMONEY = 500
MINBET = 50
WIN = 50000

#blackjack game from command line
#game steps:
'''
   Game Steps:

   1) dealer and player each get two cards from 52 card deck
   2) pl has default amount of 'money' to bet
   3) pl selects amount to bet (there is a min bet)
   4) 1 d, 1 p, 1 d, 1 p append random selected card from deck. remove card from deck.
   5) print dealer and player cards
   5) if player was dealt black jack payout is 2:1
   6) ask if user wants to bet more (check rule on this)
   7) ask if user wants to hit, fold, split, or rest (check name on this)
   8) if dealer is under 16, hit dealer
   9) execute player's choice
   10)if player hit or split, ask if they wish to hit, fold, split or rest again
   11)execute player's choice
   12)play out win/lose
'''
#TODO: write argparse argument to allow player to set initial money(?)

def welcome(money = 500) -> None:
    print(f'''
    Welcome to Matagorda Command Line BlackJack!(TM)
    We're happy to have you down today at the Dead Trout: Matagorda's Premium
    Gambling Establisment!

    I see you brought ${money} with you today. That's good, because money is 
    what we accept! (Sorry, we no longer take fish as a form of payment.)

    Come on up to our cosy table and order a drink from the pretty gal with
    most of her teeth.
    
    Please enter your initial bet! (min {MINBET}):
    ''')
    #TODO: write prompt to explain rules or start game.
    return None

def card_round(money: int) -> int:
    bet = int(input(f"Place your bet! (min {MINBET} to max {money}): "))
    while (MINBET > bet or bet > money):
        bet = int(input("I'm sorry, please enter your bet again as an int: (min $50): "))
    money -= bet
    print(f'''
    Thank you! You placed {bet}, leaving you {money}. Let's see what lady luck has
    in store for you tonight!
    ''')

    deck = shuffle_deck(DECK)
    dealer, player = deal(deck)

    print_hand_status(dealer, player)

    if value_of_hand(player) == 21:
        print(f"You were dealt a natural blackjack! You win {NATURAL_PAYOUT * bet}")
        money += int(round((NATURAL_PAYOUT + 1)* bet))
        #plus one bc you get your original bet back.
        return money
    
    #TODO: write choices (split, stand, hit, doubledown)
    #TODO: ask users for choice
    #TODO: process choice
    return money

def next_round(
        prompt: str,
        retries=4,
        reminder= "Sorry, I didn't understand. Please enter again - Y/N: "
        )-> bool:

    while True:
        ok = str(input(prompt)).lower()
        if ok in {'y','ye','yes'}:
            return True
        if ok in {'n','no','nop','nope'}:
            return False
        retries -= 1
        if retries < 0:
            raise ValueError('invalid user response')
    return False

def main():
    money = deepcopy(INITIALMONEY)
    welcome(money)
    another_round = True
    while another_round:
        money = card_round(money)
        print(f"You take a sip of your drink. You now have {money}")
        if money > WIN:
            #TODO: make a list of possible winning messages
            print('''
            The dealer looks at the stack of coins sitting next to you.
            He nods and hits a small, red button on the corner
            of his table.

            A man in a black jacket and cowboy hat walks in and sighs.

            Turns out Dead Trout of Matagorda was already living on a
            prayer, and you done cleaned her out.

            The man in the black jacket gives you a pile of cash plus 
            an IOU, shakes your hand, and escorts you out.

            'Don't come back, you hear?'

            I don't think you'll see the cash on that IOU.

            YOU WIN THE GAME!
            ''')
        elif money >= 50:
            #TODO: make list of possible messages to print on screen.
            another_round = next_round("Another Round? Y/N: ")
        else:
            #TODO: sad goodbye messages.
            print("Alas, You are only a winner in empty wallets. GAME OVER")
            another_round = False
    return 1

if __name__ == '__main__':
    sys.exit(main())
