# poker-stacking-suite
* Don't forget to star the repo if you think this is mildly interesting!

This is the github repo to make sure you always win in poker by stacking the deck while minimally moving cards around (If you are player number 1).

So far, all decks have been shown to be malleable in at least 2 moves, and no counterexample of decks where at minimum 3 moves are needed have been found.

This means that if you have a fully shuffled, random deck. By picking out just 2 cards and placing them somewhere else in the deck, you are able to create a new deck you ALWAYS win in.

Mostly for simplicity, we assume only the situation that you are always player number 1.

If you believe you have found such a deck, that 3 moves MUST be necessary to stack the deck in your favour, please open an issue in this repo, or comment here:

https://mathoverflow.net/questions/503414/worst-case-number-of-single-card-insertions-to-force-player-1-to-be-the-unique-w


# This repo contains:
A test suite and multi solver to stack a deck in your favor.
- For fully verifying all 2-moves; `brute_force_solution_v2.py`
- For a reasonably fast solver, see `solution.py`

- For the test decks and where scripts are ran, see `test.py`
- for additional utilities used in testing, see `testing_suite.py`

# If you want to check a deck:
1. Please clone this repo on your device.
2. Create a new DECK_TEST = [] with the given format of deck
3. Run the deck against the given brute force solver imported from brute_force_solution_v2.py
