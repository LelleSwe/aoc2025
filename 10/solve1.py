from itertools import product

def readlines():
    lines = []
    try:
        while (x := input().strip()):
            lines.append(x)
    except:
        pass
    return lines

def target_to_int(str_):
    str_ = str_.split("]")[0][1:]
    return (len(str_), sum([(1*2**i if a == "#" else 0) for i, a in enumerate(str_)]))

def conds_to_list(inp):
    paren = []
    curly = []

    while ")" in inp:
        first = inp.split(")", 1)[0].split("(", 1)[1]
        inp = inp.split(")", 1)[1]
        paren.append(eval("[" + first + "]"))
    
    while "}" in inp:
        first = inp.split("}", 1)[0].split("{", 1)[1]
        inp = inp.split("}", 1)[1]
        curly.append(eval("[" + first + "]"))

    return paren, curly

def list_to_int(lst):
    # print(lst)
    return list(map(lambda www: sum([1 << (a) for a in www]), lst))

inp = readlines()
targets = list(map(target_to_int, inp))
parens = list(map(lambda x: list_to_int((conds_to_list(x))[0]), inp))

def brute_one(lst, maps):
    # print(lst)
    # print(maps)
    leng = lst[0]
    lst = lst[1]
    for moves in sorted(product([0, 1], repeat=len(maps)), key=lambda x: x.count(1)):
        start = 0
        for i, move in enumerate(moves):
            start ^= move * maps[i]
        if start == lst:
            # print(moves)
            return moves.count(1)
    else:
        exit("uh oh")

def brute_all(targets, parens):
    sol = 0
    for target, paren in zip(targets, parens):
        # print("==")
        cost = brute_one(target, paren)
        sol += cost
        # print(cost)

    return sol

print(brute_all(targets, parens))
