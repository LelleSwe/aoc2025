from sage.all import *

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

def milp_one(curly, paren):
    p = MixedIntegerLinearProgram()
    t = p.new_variable(integer=True, nonnegative=True)
    curly_idxs = [t[i] for i in range(len(paren))]
    # sol = t[-1]
    # print(f"{len(curly_idxs) = }")
    
    # eqs = block_matrix([[curly], [paren]])
    eqs = matrix(paren).T
    # print(eqs)

    constraints = [curly[i] - sum([x*e for x, e in zip(curly_idxs, eq)]) == 0 for i, eq in enumerate(eqs)]
    for constraint in constraints:
        # print(constraint)
        p.add_constraint(constraint)
    p.set_objective(-sum(curly_idxs))

    sol = p.solve()
    # print(-ZZ(sol))
    # print(p.get_values())
    # print(p.get_min(sol))
    # for cons in curly_idxs:
    #     w = p.get_values(cons, tolerance=0.1, convert=ZZ)
    #     # print(type(w), w)

    return -ZZ(sol)

def brute_all(curlys, parens):
    sol = 0
    works = 0
    for i, curly, paren in zip(range(2**32), curlys, parens):
        cost = milp_one(curly, paren)
        if cost == None:
            # print(f"pass {i+1} out of {len(curlys)} failed")
            continue
        works += 1
        sol += cost
        # print(cost)

    return sol

print(brute_all(curlys, parens_pad))
