RANK_VALUE = {"2":2,"3":3,"4":4,"5":5,"6":6,"7":7,"8":8,"9":9,"10":10,"J":11,"Q":12,"K":13,"A":14}
SUIT_MAP = {"♣":0,"♦":1,"♥":2,"♠":3}

def _parse_card(cs): return RANK_VALUE[cs[1:]], SUIT_MAP[cs[0]]
def _build_arrays(deck):
    ranks=[0]*52; suits=[0]*52
    for i,cs in enumerate(deck):
        r,s=_parse_card(cs); ranks[i]=r; suits[i]=s
    return ranks,suits

def _score7(c0,c1,c2,c3,c4,c5,c6,ranks,suits):
    cnt=[0]*15; sc=[0,0,0,0]; sb=[0,0,0,0]; rb=0
    for cid in (c0,c1,c2,c3,c4,c5,c6):
        r=ranks[cid]; s=suits[cid]
        cnt[r]+=1; sc[s]+=1; sb[s]|=1<<r; rb|=1<<r
    def sh(bits):
        if bits&(1<<14): bits|=1<<1
        for h in range(14,4,-1):
            m=(1<<h)|(1<<(h-1))|(1<<(h-2))|(1<<(h-3))|(1<<(h-4))
            if (bits&m)==m: return h
        return 0
    fs=-1
    if sc[0]>=5: fs=0
    elif sc[1]>=5: fs=1
    elif sc[2]>=5: fs=2
    elif sc[3]>=5: fs=3
    if fs!=-1:
        fb=sb[fs]; t=sh(fb)
        if t: return (8<<20)|(t<<16)
        top=[]; 
        for r in range(14,1,-1):
            if fb&(1<<r):
                top.append(r)
                if len(top)==5: break
        return (5<<20)|(top[0]<<16)|(top[1]<<12)|(top[2]<<8)|(top[3]<<4)|top[4]
    quads=0; trips=[]; pairs=[]; singles=[]
    for r in range(14,1,-1):
        c=cnt[r]
        if c==4: quads=r
        elif c==3: trips.append(r)
        elif c==2: pairs.append(r)
        elif c==1: singles.append(r)
    if quads:
        k= singles[0] if singles else (pairs[0] if pairs else (trips[0] if trips else 0))
        return (7<<20)|(quads<<16)|(k<<12)
    if trips:
        pr=0
        if len(trips)>=2: pr=trips[1]
        elif pairs: pr=pairs[0]
        if pr: return (6<<20)|(trips[0]<<16)|(pr<<12)
        k1=singles[0] if singles else 0
        k2=singles[1] if len(singles)>1 else (pairs[0] if pairs else 0)
        return (3<<20)|(trips[0]<<16)|(k1<<12)|(k2<<8)
    t=sh(rb)
    if t: return (4<<20)|(t<<16)
    if len(pairs)>=2:
        k=singles[0] if singles else (pairs[2] if len(pairs)>2 else 0)
        return (2<<20)|(pairs[0]<<16)|(pairs[1]<<12)|(k<<8)
    if len(pairs)==1:
        k1=singles[0] if singles else 0
        k2=singles[1] if len(singles)>1 else 0
        k3=singles[2] if len(singles)>2 else 0
        return (1<<20)|(pairs[0]<<16)|(k1<<12)|(k2<<8)|(k3<<4)
    while len(singles)<5: singles.append(0)
    return (singles[0]<<16)|(singles[1]<<12)|(singles[2]<<8)|(singles[3]<<4)|singles[4]

def _p1_unique_wins_prefix(prefix,n,ranks,suits):
    first=prefix[:n]; second=prefix[n:2*n]; board=prefix[2*n:2*n+5]
    s1=_score7(first[0],second[0],board[0],board[1],board[2],board[3],board[4],ranks,suits)
    for p in range(1,n):
        sp=_score7(first[p],second[p],board[0],board[1],board[2],board[3],board[4],ranks,suits)
        if sp>=s1: return False
    return True

def _leaders(prefix,n,ranks,suits):
    first=prefix[:n]; second=prefix[n:2*n]; board=prefix[2*n:2*n+5]
    best=-1; win=[]
    for p in range(n):
        s=_score7(first[p],second[p],board[0],board[1],board[2],board[3],board[4],ranks,suits)
        if s>best: best=s; win=[p]
        elif s==best: win.append(p)
    return win

def _apply_move_full(ids,i,j):
    out=ids[:]; x=out.pop(i)
    if j>len(out): j=len(out)
    out.insert(j,x); return out

def _move_card_to_pos_full(ids,card,pos):
    out=ids[:]; k=out.index(card); out.pop(k)
    if k<pos: pos-=1
    if pos<0: pos=0
    if pos>len(out): pos=len(out)
    out.insert(pos,card); return out

def _index_array(arr):
    idx=[-1]*52
    for i,c in enumerate(arr): idx[c]=i
    return idx

def _remove_if_present(S,idx,card):
    k=idx[card]
    if k==-1: return
    S.pop(k); idx[card]=-1
    L=len(S)
    for m in range(k,L): idx[S[m]]-=1

def _insert_with_cap(S,idx,card,pos,cap):
    if pos>len(S): pos=len(S)
    S.insert(pos,card)
    L=len(S)
    for m in range(pos,L): idx[S[m]]=m
    if L>cap:
        rem=S.pop(); idx[rem]=-1

def stack_deck(deck,n_players):
    n=n_players; t=2*n+5
    ranks,suits=_build_arrays(deck)
    ids=list(range(52))

    if _p1_unique_wins_prefix(ids[:t],n,ranks,suits):
        return deck[:]

    def build_impact():
        first=ids[:n]; second=ids[n:2*n]; board_ids=ids[2*n:2*n+5]
        kino=(first[0],second[0]); pn=(first[n-1],second[n-1])
        winners=_leaders(ids[:t],n,ranks,suits)
        winholes=[]
        for p in winners:
            if p!=0:
                winholes.extend((first[p],second[p]))
        same=[c for c in ids if ranks[c]==ranks[kino[0]] or ranks[c]==ranks[kino[1]]]
        near=[]
        if t<52: near.append(ids[t])
        if t+1<52: near.append(ids[t+1])
        src=[]
        def add(xs):
            for x in xs:
                if x not in src: src.append(x)
        add(kino); add(board_ids); add(pn); add(winholes); add(same); add(ids[:t]); add(near)

        dst_core=[0,n]+[2*n+k for k in range(5)]
        dst_extra=[n-1,2*n-1]
        for p in winners:
            if p!=0:
                dst_extra.extend((p,n+p))
        dst=[]; seen=set()
        for d in dst_core+dst_extra:
            if 0<=d<=t and d not in seen:
                dst.append(d); seen.add(d)
        return src,dst

    src_priority,dst_priority=build_impact()

    W1=t+1;  W1=52 if W1>52 else W1
    base1=ids[:W1]
    pos_map={c:k for k,c in enumerate(ids)}
    for s in src_priority:
        i=pos_map[s]
        for d in dst_priority+[10**9]:
            j = W1+1 if d==10**9 else d
            if i>=t and j>=t: continue
            S=base1[:]; x=ids[i]
            if i<len(S): S.pop(i)
            jj=j if j<=len(S) else len(S)
            S.insert(jj,x)
            if len(S)>W1: S.pop()
            if _p1_unique_wins_prefix(S[:t],n,ranks,suits):
                j_full=52 if d==10**9 else d
                cand=_apply_move_full(ids,i,j_full)
                if _p1_unique_wins_prefix(cand[:t],n,ranks,suits):
                    return [deck[k] for k in cand]

    for i in range(52):
        for j in range(W1+1):
            if i>=t and j>=t: continue
            S=base1[:]; x=ids[i]
            if i<len(S): S.pop(i)
            jj=j if j<=len(S) else len(S)
            S.insert(jj,x)
            if len(S)>W1: S.pop()
            if _p1_unique_wins_prefix(S[:t],n,ranks,suits):
                cand=_apply_move_full(ids,i,j)
                if _p1_unique_wins_prefix(cand[:t],n,ranks,suits):
                    return [deck[k] for k in cand]

    boards=[2*n+k for k in range(5)]
    D2=[]; seen=set()
    for d in [0,n]+boards+[n-1,2*n-1]:
        if d not in seen: D2.append(d); seen.add(d)
    for p in _leaders(ids[:t],n,ranks,suits):
        if p!=0:
            for d in (p,n+p):
                if d not in seen: D2.append(d); seen.add(d)
    pos_pairs=[(a,b) for a in D2 for b in D2 if a!=b]

    W2=t+2; W2=52 if W2>52 else W2
    B=ids[:W2]; idx0=_index_array(B)

    order=src_priority[:] + [c for c in range(52) if c not in src_priority]
    for p1,p2 in pos_pairs:
        for a in order:
            for b in order:
                if a==b: continue
                S=B[:]; idx=idx0[:]
                _remove_if_present(S,idx,a)
                _insert_with_cap(S,idx,a,p1,W2)
                _remove_if_present(S,idx,b)
                _insert_with_cap(S,idx,b,p2,W2)
                if _p1_unique_wins_prefix(S[:t],n,ranks,suits):
                    cand=_move_card_to_pos_full(ids,a,p1)
                    cand=_move_card_to_pos_full(cand,b,p2)
                    if _p1_unique_wins_prefix(cand[:t],n,ranks,suits):
                        return [deck[k] for k in cand]

    print("no 2 card found, is this the famed 3 card setup?")
    return deck[:]
