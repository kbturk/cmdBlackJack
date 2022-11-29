import sys
from BlackJackLib import *
import argparse

#blackjack game from command line
#game steps:
'''
   Game Steps:

   1) dealer and player each get two cards from 52 card deck
   2) pl has default amount of 'money' to bet
   3) pl selects amount to bet (there is a min bet)
   4) 1 d, 1 p, 1 d, 1 p append random selected card from deck. remove card from deck.
   5) print dealer and player cards
   6) if player was dealt black jack payout is {NATURAL_PAYOUT}
   7) ask if user wants to bet more
   8) ask if user wants to hit, stay, double, or split
   9) if dealer is under 16, hit dealer
   10)execute player's choice
   11)play out win/lose
   12)ask if user wants to play another round
'''
#TODO: write argparse argument to allow player to set initial money(?)

def welcome(money = 500) -> None:
    print(f'''
    ---------------------------------------------------------------------------
    Welcome to Matagorda Command Line BlackJack!(TM)
    We're happy to have you down today at the Dead Trout: Matagorda's Premium
    Gambling Establisment!

    I see you brought ${money} with you today. That's good, because money is 
    what we accept! (Sorry, we no longer take fish as a form of payment.)

    Come on up to our cosy table and order a drink from the purdy gal with
    most of her teeth.
    ---------------------------------------------------------------------------
    ''')
    #TODO: write or give link on rules of the game.
    return None

def card_round(money: int) -> int:
    bet = accept_bet(f"    Place your bet! (min {MINBET} to max {money}): ", money)
    money -= bet
    print(f'''
    ---------------------------------------------------------------------------
    Thank you! You placed {bet}, leaving you {money}.
    Let's see what lady luck has in store for you tonight!
    ---------------------------------------------------------------------------
    ''')

    deck = shuffle_deck(DECK)
    dealer, player = deal(deck)
    deck = deck[3:] #remove first 4 cards
    print_hand_status(dealer, player)

    if is_natural_blackjack(player) and value_of_hand(dealer) != 21:
        print(f"\tYou were dealt a natural blackjack! You win {NATURAL_PAYOUT * bet}")
        money += int(round((NATURAL_PAYOUT + 1)* bet))
        #plus one bc you get your original bet back.
        return money

    sp: bool = False
    bet2 = 0
    if can_split_pairs(player) and money - bet > 0:
        if ask_ok("    Would you like to split your pairs? Split/No: ",
                yes = {'split','y','s','ye','yes', 'sp'}):
            money -= bet
            bet2 = bet
            print(f"    You slap another ${bet} on the table. You now have {money} left.")
            sp = True

    dd: bool = False
    if can_double_down(player) and money - bet > 0:
        if ask_ok("    Would you like to double down? DD/N: ",
                yes = {'y','ye','yes','d','double down','dd'}):
            money -= bet
            bet *= 2
            dd = True

    player, deck, player2 = player_turn(player, dealer, deck, dd, sp)

    if sp:
        if value_of_hand(player) > 21 and value_of_hand(player2) > 21:
            print("\tYou bust on both hands. The House takes your hard earned money.\n")
            return int(money)
        elif value_of_hand(player) > 21:
            print("\tYou bust on the first hand. Let's see how the other does.\n")
            bet = 0 #downsize your bet
        elif value_of_hand(player2) > 21:
            print("\tYou bust on the second hand. Let's see how the other does.\n")
            bet2 = 0 #downsize your bet
    else:
        if value_of_hand(player) > 21:
            print("\tYou bust. The House takes your hard earned money.\n")
            return int(money)

    print(f'''
    ---------------------------------------------------------------------------
    The Dealer takes their turn. They flip over their hidden card.\n''')

    dealer, deck = dealer_turn(dealer, deck)
    print_hand_status(dealer, player, player2 = player2, dealer_hidden = False)

    if value_of_hand(dealer) > 21:
        print("\tThe Dealer busts. The purdy girl brings you another drink.\n")
        return int(money + 2*(bet + bet2))

    #hand1 winner/loser outcome:
    winner = player_win(player, dealer)

    #optional hand2 winner/loser outcome:
    if player2 is not None and value_of_hand(player) <= 21:
        winner2 = player_win(player2, dealer)
        print("\tHand1 results:")
    else:
        winner2 = False

    if winner is None:
        money += bet
        print("\tLooks like a draw partner. Here's your money back\n")
    elif winner:
        money += 2*bet
        print("\tYou win the hand! The Dealer tosses you your winnings.\n")
    else:
        print("\tYou shake your head. The Dealer takes your chips.\n")

    if player2 is not None and value_of_hand(player) <= 21:
        print("\tHand2 results:")
        if winner2 is None:
            money += bet
            print("\tLooks like a draw partner. Here's your money back\n")
        elif winner:
            money += 2*bet2
            print("\tYou win the hand! The Dealer tosses you your winnings.\n")
        else:
            print("\tYou shake your head. The Dealer takes your chips.\n")

    return money

def main():
    money = deepcopy(INITIALMONEY)
    welcome(money)
    another_round = True
    while another_round:
        money = card_round(money)
        print(f"\tYou take a sip of your drink. You now have ${money}\n")
        if money >= WIN:
            #TODO: make a list of possible winning messages
            print('''
    The Dealer looks at the stack of coins sitting next to you.
    He nods and hits a small, red button on the corner of his table.

    A man in a black jacket and cowboy hat walks in and sighs.

    Turns out Dead Trout of Matagorda was already living on a prayer, and you
    done cleaned her out.

    The man in the black jacket gives you a pile of cash plus an IOU.

    He begrudedly shakes your hand.'Don't come back, you hear?'

    You leave, satisfied but knowing you won't see the cash on that IOU.
    You leave a 1-star trip review.

    YOU WIN THE GAME!''')
        elif money >= 50:
            #TODO: make list of possible messages to print on screen.
            another_round = ask_ok("    Another Round? Y/N: ")
        else:
            #TODO: sad goodbye messages.
            print("\tAlas, You are only a winner in empty wallets. GAME OVER")
            another_round = False
            return 1
    print(f'''
    ---------------------------------------------------------------------------
    You feel something shift in the universe: the open road is calling. You put
    down your drink. You scoop up your winnings, tossing the dealer ${int(round(money*.05))}. 
    They nodd to you. You take the remaining to the teller.

    You leave with ${int(round(money*.95))}

    THANKS FOR PLAYING
    ---------------------------------------------------------------------------
    ''')
    return 1

if __name__ == '__main__':
    sys.exit(main())
