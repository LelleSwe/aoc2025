# LLL time >:)
from sage.all import *
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

def paren_conv(lst, leng):
    ret = [[0] * leng for _ in range(len(lst))]
    for i, l in enumerate(lst):
        for val in l:
            ret[i][val] = 1

    return ret

inp = readlines()
targets = list(map(target_to_int, inp))
parens = list(map(lambda x: conds_to_list(x)[0], inp))
curlys = list(map(lambda x: conds_to_list(x)[1][0], inp))
parens_pad = []
for paren, curly in zip(parens, curlys):
    parens_pad.append(paren_conv(paren, len(curly)))
# print(f"{parens = }")
# print(f"{parens_pad = }")

def lll_one(curly, paren):
    M = block_matrix(
        [
            [-16*matrix(curly), -0*matrix([1] * len(paren)), 2**20], 
            [16*matrix(paren), 2*identity_matrix(len(paren)), 0]
        ]
    )

    # M.extend(paren)
    # M = matrix(M)
    # print(M)
    # exit()
    B, L = M.LLL(transformation=True)
    failed = False
    if not all(list(map(lambda x: x == 0, B[-1][:len(curly)]))):
        failed = True
        # print(B[-1][:len(curly)])
    if not all(list(map(lambda x: x >= 0, L[-1][:len(curly)]))):
        failed = True
        # print(L[-1][:len(curly)])
    if failed:
        # print("Failed!")
        return None

    # print(B)
    # print()
    # print(L)
    # print(sum(L[-1][1:]))
    # exit()
    return sum(L[-1][1:])
    # 16711 is too high!
    pass

def brute_all(curlys, parens):
    sol = 0
    works = 0
    for i, curly, paren in zip(range(2**32), curlys, parens):
        cost = lll_one(curly, paren)
        if cost == None:
            # print(f"pass {i+1} out of {len(curlys)} failed")
            continue
        works += 1
        sol += cost
        # print(cost)

    print(f"LLL passes (gives reasonable output for?) {works} cases out of {len(curlys)}")
    return sol

print(brute_all(curlys, parens_pad))
