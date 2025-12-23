def readlines():
    lines = []
    try:
        while (x := input().strip()):
            if x == "":
                break
            lines.append(x)
    except:
        pass

    return lines

def parse(lines):
    state_e = {}
    state_s = {}
    pmap = {}
    counter = 0
    for line in lines:
        start = line.split(": ")[0]
        ends = line.split(": ")[1].split()
        # print(start, ends)
        
            # print("yeyeye")

        if start not in pmap:
            pmap[start] = counter
            # print(start, counter)
            counter += 1
        for end in ends:
            if end not in pmap:
                pmap[end] = counter
                # print(end, counter)
                counter += 1
            
            if pmap[end] not in state_e:
                state_e[pmap[end]] = [pmap[start]]
            else:
                state_e[pmap[end]].append(pmap[start])

        state_s[pmap[start]] = list(map(lambda x: pmap[x], ends))
    for w in pmap.values():
        if w not in state_s:
            state_s[w] = []
        if w not in state_e:
            state_e[w] = []
    # print(counter, len(pmap))
    # print(pmap)
    # state[w] = [all that map to w]
    from_ = sorted(list(state_e.items()), key = lambda x: x[0])
    # print(f"{from_ = }")
    # state[w] = [all that w map to]
    to_   = sorted(list(state_s.items()), key = lambda x: x[0])
    # print(f"{to_ = }")

    sc = pmap["svr"] 
    ec = pmap["out"] 
    dac = pmap["dac"] 
    fft = pmap["fft"] 

    return sc, ec, dac, fft, list(map(lambda x: x[1], from_)), list(map(lambda x: x[1], to_))

def topsort(graph):
    res, found = [], [0] * len(graph)
    stack = list(range(len(graph)))
    while stack:
        node = stack.pop()
        if node < 0:
            res.append(~node)
        elif not found[node]:
            found[node] = 1
            stack.append(~node)
            stack += graph[node]
    # print(f"{res = }")
    # print(f"{found = }")


    # cycle check
    for node in res:
        if any(found[nei] for nei in graph[node]):
            # print(f"{[found[nei] for nei in graph[node]] = }")
            # print(f"{node = }")
            return None
        found[node] = 0

    return res

lines = readlines()
# print(lines)
sc, ec, dac, fft, from_, to_ = parse(lines)
print(f"{sc, ec, dac, fft = }")

# print(f"{from_ = }")
order = topsort(from_)
# print(f"{order = }")

def clear_state(order):
    state = {}
    for p in order:
        state[p] = 0
    return state

def solve(order, graph, start, end, dac, fft):
    state = clear_state(order)
    state[start] = 1 # you start here

    for p in order:
        if p == dac:
            val = state[p]
            # print(f"dac {val}")
            state = clear_state(order)
            state[p] = val
        if p == fft:
            val = state[p]
            state = clear_state(order)
            state[p] = val
            # print(f"fft {val}")
        for p2 in graph[p]:
            state[p2] += state[p]

    # print(f"{state = }")
    return state[end]

sol = solve(order, to_, sc, ec, dac, fft)
print(sol)
