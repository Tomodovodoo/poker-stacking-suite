from solution import stack_deck
from testing_suite import _is_permutation, _kino_wins_bool, _count_moves_minimal
from brute_force_solution_v2 import brute_force_check as stack_deck_v3


DECK_TEST1 = [
 '♣6','♥2','♠2','♣Q','♠Q','♦K','♣10','♠K','♠10','♣9','♠J','♠7','♥7',    # round 1: P1..P13
 '♠3','♠5','♦5','♥J','♦A','♥Q','♥A','♣A','♦J','♥10','♦2','♥3','♦4',   # round 2: P1..P13
 '♠A','♥K','♦Q','♣J','♦10',               # board: A K Q J T
 '♣K','♦9','♥9','♠9',                # rest of deck (arbitrary fill)
 '♣8','♦8','♥8','♠8',
 '♣7','♦7',
 '♦6','♥6','♠6',
 '♣5','♥5',
 '♣4','♥4','♠4',
 '♣3','♦3',
 '♣2'
]


DECK_TEST = [
 '♣6','♥2','♠2','♥A','♣A','♦A','♣Q','♠A','♣10','♠Q','♠10','♥3','♣7','♥7',    # round 1: P1..P14
 '♠3','♠5','♦5','♥10','♦K','♥Q','♥J','♥K','♦J','♠K','♠J','♣9','♦4','♦2',   # round 2: P1..P14
 '♦Q','♣J','♣K','♦10','♠7',            # board: K Q J T 7
 '♦7','♠4',                            #padding
 '♦9','♥9','♠9',                # rest of deck (arbitrary fill)
 '♣8','♦8','♠8','♥8',
 '♦6','♥6','♠6',
 '♣5','♥5',
 '♣4','♥4',
 '♣3','♦3',
 '♣2'
]

DECK_TEST3 = [
'♥3','♣10','♠J','♠Q','♣K','♠K','♥Q','♦J',  # ID 7
'♣7','♠A','♦A','♣A','♥A','♦K','♣Q','♣J',   # ID 15
'♣2','♠10','♥J','♦Q','♥K',                 # ID 20
'♥2','♦2','♠2',
'♦3','♠3','♣3',
'♥4','♦4','♠4','♣4',
'♥5','♦5','♠5','♣5',
'♥6','♦6','♠6','♣6',
'♥7','♦7','♠7',
'♥8','♦8','♠8','♣8',
'♥9','♦9','♠9','♣9',
'♥10','♦10'
]


DECK_TEST4 = [
 '♣6','♥2','♦A','♣A','♦K','♣Q','♠10','♣9',     # round 1: P1..P7
 '♠3','♠5','♠Q','♠K','♥Q','♥J','♦J','♥10',     # round 2: P1..P7
 '♠A','♥K','♦Q','♣J','♦10',               # board: A K Q J T
 '♠J','♣10',                               # the next two replacements if cards are moved past community cards (J, T)
 '♥A','♣K','♦9','♥9','♠9',                # rest of deck (arbitrary fill)
 '♣8','♦8','♥8','♠8',
 '♣7','♦7','♥7','♠7',
 '♦6','♥6','♠6',
 '♣5','♦5','♥5',
 '♣4','♦4','♥4','♠4',
 '♣3','♥3','♦3',
 '♣2','♦2','♠2'
]




FULL_DECK = [
'♥2','♦2','♠2','♣2',
'♥3','♦3','♠3','♣3',
'♥4','♦4','♠4','♣4',
'♥5','♦5','♠5','♣5',
'♥6','♦6','♠6','♣6',
'♥7','♦7','♠7','♣7',
'♥8','♦8','♠8','♣8',
'♥9','♦9','♠9','♣9',
'♥10','♦10','♠10','♣10',
'♥J','♦J','♠J','♣J',
'♥Q','♦Q','♠Q','♣Q',
'♥K','♦K','♠K','♣K',
'♥A','♦A','♠A','♣A'
]



VERBOSE = True


if __name__ == "__main__":
    orig, players = DECK_TEST[:], 14
    new_deck = stack_deck_v3(orig[:], players)
    if _is_permutation(orig, new_deck) == False:
        print(f"Test not passed; permutation of deck; Deck does not contain 52 unique cards!")
    if _kino_wins_bool(new_deck, players, VERBOSE) == False:
            print(f"Your solution does not make Kino win, WTF?!")
    minimal_moves = _count_moves_minimal(orig, new_deck)
    print(f"Our solution found the minimal amount of moves to be {minimal_moves}!")