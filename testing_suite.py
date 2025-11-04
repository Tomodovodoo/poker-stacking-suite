RANKS = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":11,"Q":12,"K":13,"A":14}

def _split(card):
    return card[0], card[1:]

def _holes_and_board(deck, players):
    assert 2*players + 5 <= len(deck)
    holes = [[deck[i], deck[players + i]] for i in range(players)]
    board = deck[2*players : 2*players + 5]
    return holes, board

def _rank_five(cards):
    from collections import Counter
    suits = [ _split(c)[0] for c in cards ]
    ranks = [ RANKS[_split(c)[1]] for c in cards ]
    ranks.sort(reverse=True)
    cnt = Counter(ranks)

    def is_straight(vals):
        v = sorted(set(vals))
        if len(v) != 5:
            return False, None
        if v[-1] - v[0] == 4:
            return True, v[-1]
        if set(v) == {14, 5, 4, 3, 2}:
            return True, 5
        return False, None

    is_flush = (len(set(suits)) == 1)
    s_ok, s_high = is_straight(ranks)

    groups = sorted(((n, r) for r, n in cnt.items()), reverse=True)
    if is_flush and s_ok:
        return (8, (s_high,))
    if groups[0][0] == 4:
        four = groups[0][1]
        kicker = max(r for r in ranks if r != four)
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
        return (3, (three,) + tuple(sorted(ks, reverse=True)[:2]))
    if groups[0][0] == 2 and groups[1][0] == 2:
        p_hi = max(groups[0][1], groups[1][1])
        p_lo = min(groups[0][1], groups[1][1])
        kicker = max(r for r in ranks if r != p_hi and r != p_lo)
        return (2, (p_hi, p_lo, kicker))
    if groups[0][0] == 2:
        p = groups[0][1]
        ks = [r for r in ranks if r != p]
        return (1, (p,) + tuple(sorted(ks, reverse=True)[:3]))
    return (0, tuple(sorted(ranks, reverse=True)))

def _best_holdem_rank(hole, board):
    from itertools import combinations
    best = None
    seven = hole + board
    for combo in combinations(seven, 5):
        r = _rank_five(list(combo))
        if best is None or r > best:
            best = r
    return best

def _kino_wins_bool(deck, players, verbose):
    holes, board = _holes_and_board(deck, players)
    if verbose:
        deal1 = deck[:players]
        deal2 = deck[players:2*players]
        comm  = deck[2*players:2*players+5]
        rest  = deck[2*players+5:]
        print(deal1)
        print(deal2)
        print(comm)
        print(rest)
        print(f"Community cards: {board}")
        cat_name = {
            8: "Straight Flush",
            7: "Four of a Kind",
            6: "Full House",
            5: "Flush",
            4: "Straight",
            3: "Three of a Kind",
            2: "Two Pair",
            1: "One Pair",
            0: "High Card",
        }


    all_ranks = []
    for i in range(players):
        r = _best_holdem_rank(holes[i], board)
        all_ranks.append(r)
        if verbose:
            if i == 0:
                print(f"Kino: hole {holes[i]} -> {cat_name[r[0]]} {r[1]}")
            else:
                print(f"'Friend' {i}: hole {holes[i]} -> {cat_name[r[0]]} {r[1]}")

    kino = all_ranks[0]
    best_other = max(all_ranks[1:]) if players > 1 else None
    return best_other is None or (kino is not None and kino > best_other)


def _is_permutation(a, b):
    return sorted(a) == sorted(b)

def _count_moves_minimal(orig, new):
    pos = {c: i for i, c in enumerate(orig)}
    seq = [pos[c] for c in new]

    import bisect

    n = len(seq)
    tails = []
    tails_idx = []
    prev = [-1] * n

    for i, x in enumerate(seq):
        j = bisect.bisect_left(tails, x)
        if j == len(tails):
            tails.append(x)
            tails_idx.append(i)
        else:
            tails[j] = x
            tails_idx[j] = i
        if j > 0:
            prev[i] = tails_idx[j - 1]

    lis_indices = []
    if tails_idx:
        k = tails_idx[-1]
        while k != -1:
            lis_indices.append(k)
            k = prev[k]
        lis_indices.reverse()
    lis_set = set(lis_indices)

    moved = [ (new[i], pos[new[i]], i) for i in range(n) if i not in lis_set ]
    if moved:
        print("Moved cards (orig_idx->new_idx): " +
              ", ".join(f"{c} [{oi}->{ni}]" for c, oi, ni in moved))
    else:
        print("Moved cards: []")

    return len(orig) - len(lis_indices)