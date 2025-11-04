
# Collects winning candidates; then among those with minimal k picks the
# strongest solution. Prints totals and chosen move sequence.

from typing import List, Tuple
from functools import lru_cache
from itertools import combinations

RANKS = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":11,"Q":12,"K":13,"A":14}
SUITS = ("♣","♦","♥","♠")

def _split(card: str) -> Tuple[str, str]:
    if len(card) >= 3 and card[1:3] == "10":
        return (card[0], "10")
    return (card[0], card[1:])


@lru_cache(maxsize=1_000_000)
def _rank_five_sorted_key(key: Tuple[str, str, str, str, str]) -> Tuple[int, Tuple[int, ...]]:
    suits = []
    ranks = []
    for c in key:
        s, r = _split(c)
        suits.append(s)
        ranks.append(RANKS[r])
    ranks.sort(reverse=True)

    def _is_straight(vals):
        v = sorted(set(vals))
        if len(v) != 5:
            return False, None
        if v[-1] - v[0] == 4:
            return True, v[-1]
        if set(v) == {14,5,4,3,2}:
            return True, 5
        return False, None

    is_flush = (len(set(suits)) == 1)
    s_ok, s_high = _is_straight(ranks)
    counts = {}
    for r in ranks:
        counts[r] = counts.get(r, 0) + 1
    groups = sorted(((cnt, r) for r, cnt in counts.items()), reverse=True)

    if is_flush and s_ok:
        return (8, (s_high,))
    if groups[0][0] == 4:
        four = groups[0][1]
        kicker = next(r for r in ranks if r != four)
        return (7, (four, kicker))
    if groups[0][0] == 3 and groups[1][0] == 2:
        return (6, (groups[0][1], groups[1][1]))
    if is_flush:
        return (5, tuple(sorted(ranks, reverse=True)))
    if s_ok:
        return (4, (s_high,))
    if groups[0][0] == 3:
        three = groups[0][1]
        ks = [r for r in ranks if r != three]
        ks.sort(reverse=True)
        return (3, (three, ks[0], ks[1]))
    if groups[0][0] == 2 and groups[1][0] == 2:
        p_hi = max(groups[0][1], groups[1][1])
        p_lo = min(groups[0][1], groups[1][1])
        kicker = max(r for r in ranks if r != p_hi and r != p_lo)
        return (2, (p_hi, p_lo, kicker))
    if groups[0][0] == 2:
        p = groups[0][1]
        ks = [r for r in ranks if r != p]
        ks.sort(reverse=True)
        return (1, (p, ks[0], ks[1], ks[2]))
    return (0, tuple(sorted(ranks, reverse=True)))

_COMB_7C5 = tuple(combinations(range(7), 5))
@lru_cache(maxsize=1_000_000)
def _best7_rank_from_sorted7(sorted7: Tuple[str, ...]) -> Tuple[int, Tuple[int, ...]]:
    cards = list(sorted7)
    best = None
    for idxs in _COMB_7C5:
        key5 = tuple(sorted(cards[i] for i in idxs))
        r = _rank_five_sorted_key(key5)
        if best is None or r > best:
            best = r
    return best

def _best_holdem_rank(hole: Tuple[str, str], board: Tuple[str, ...]) -> Tuple[int, Tuple[int, ...]]:
    seven = tuple(sorted((hole[0], hole[1], *board)))
    return _best7_rank_from_sorted7(seven)

def _holes_and_board_from_head(head_key: Tuple[str, ...], players: int):
    p = players
    d1 = head_key[:p]
    d2 = head_key[p:2*p]
    holes = tuple((d1[i], d2[i]) for i in range(p))
    board = tuple(head_key[2*p:2*p+5])
    return holes, board

@lru_cache(maxsize=500_000)
def _kino_wins_head_key(head_key: Tuple[str, ...], players: int) -> bool:
    holes, board = _holes_and_board_from_head(head_key, players)
    ranks = tuple(_best_holdem_rank(holes[i], board) for i in range(players))
    kino = ranks[0]
    best_other = max(ranks[1:]) if players > 1 else None
    return (best_other is None) or (kino is not None and kino > best_other)

@lru_cache(maxsize=500_000)
def _p1_rank_head_key(head_key: Tuple[str, ...], players: int) -> Tuple[int, Tuple[int, ...]]:
    holes, board = _holes_and_board_from_head(head_key, players)
    return _best_holdem_rank(holes[0], board)

def _kino_wins_bool(deck: List[str], players: int, verbose: bool=False) -> bool:
    head_len = 2*players + 5
    return _kino_wins_head_key(tuple(deck[:head_len]), players)

def _p1_rank(deck: List[str], players: int) -> Tuple[int, Tuple[int, ...]]:
    head_len = 2*players + 5
    return _p1_rank_head_key(tuple(deck[:head_len]), players)

def _apply_move(order: List[str], i: int, j: int) -> List[str]:
    if j == i or j == i + 1:
        return order
    x = order[i]
    if j > i:
        j -= 1
    new = order[:i] + order[i+1:]
    if j < 0:
        j = 0
    new.insert(j, x)
    return new

def brute_force_check(deck: List[str], n_players: int) -> List[str]:


    """Collects  solutions; prints count and the chosen strongest among minimal k, then returns it.
    If none within 2 moves, prints "3 card found!!!" and returns the original deck.
    """
    n = n_players
    N = len(deck)
    HEAD_PLAY = 2*n + 7           # number of cards in the "play area"
    HEAD_LEN = HEAD_PLAY
    DISCARD = N + 1

    solutions: List[Tuple[int, Tuple[Tuple[int,int], ...], List[str]]] = []

    if _kino_wins_bool(deck, n, False):
        solutions.append((0, tuple(), deck[:]))

    dests_first = list(range(0, HEAD_LEN + 1)) + [DISCARD]
    dests_second = list(range(0, HEAD_LEN + 1))

    def affects_head(i: int, j: int) -> bool:
        if i >= HEAD_LEN and j > HEAD_LEN:
            return False
        return True

    # k = 1
    for i in range(N):
        for j in dests_first:
            if j == i or j == i + 1:
                continue
            if not affects_head(i, j):
                continue
            d1 = _apply_move(deck, i, j)
            if _kino_wins_bool(d1, n, False):
                solutions.append((1, ((i, j),), d1))

    # k = 2
    for i in range(N):
        print(i)
        for j in dests_first:
            if j == i or j == i + 1:
                continue
            if not affects_head(i, j):
                continue
            d1 = _apply_move(deck, i, j)
            moved_card = deck[i]
            for p in range(N):
                if d1[p] == moved_card:
                    continue
                for q in dests_second:
                    if q == p or q == p + 1:
                        continue
                    if not affects_head(p, q):
                        continue
                    d2 = _apply_move(d1, p, q)
                    if _kino_wins_bool(d2, n, False):
                        solutions.append((2, ((i, j), (p, q)), d2))

    if solutions:
        min_k = min(k for (k, _, _) in solutions)
        mins = [(moves, d) for (k, moves, d) in solutions if k == min_k]
        best_moves, best_deck = max(
            mins,
            key=lambda md: (_p1_rank(md[1], n), md[0])
        )
        print(f"[Brute] total solutions found: {len(solutions)}")
        print(f"[Brute] chosen k={min_k} moves={list(best_moves)}")
        return best_deck

    print("3 card found!!!")
    return deck
