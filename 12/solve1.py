def readlines():
    lines = []
    try:
        while True:
            lines.append(input().strip())
    except EOFError as e:
        pass
    return lines

def parse_structs(lines):
    structs = []
    lines = iter(lines)
    for _ in range(6):
        next(lines)
        box = []
        for _ in range(3):
            inp = next(lines)
            box.append(list(map(lambda x: 1 if x == "#" else 0, inp)))
        next(lines)
        structs.append(box)
    return structs

def parse_trees(lines):
    lines = iter(lines)
    dimss = []
    typess = []
    try:
        while (line := next(lines)):
            first = line.split(": ")[0]
            second = line.split(": ")[1]

            dims = list(map(int, first.split("x")))
            types = list(map(int, second.split()))
            dimss.append(dims)
            typess.append(types)
    except:
        pass

    return dimss, typess

def idiot_solve(dimss, typess):
    works = 0
    not_works = 0
    for dims, types in zip(dimss, typess):
        if (dims[0] // 3) * (dims[1] // 3) >= sum(types):
            works += 1
        else:
            not_works += 1

    return works, not_works # 487 pass from just that okay

def idiot_solve2(dimss, typess, structs):
    works = 0
    not_works = 0
    per_struct = list(map(lambda xs: sum(sum(x) for x in xs), structs))
    dot_prod = lambda xs, ys: sum([x*y for x, y in zip(xs, ys)])
    for dims, types in zip(dimss, typess):
        if dims[0] * dims[1] > dot_prod(types, per_struct):
            works += 1
        else:
            not_works += 1

    return works, not_works # 513 don't pass from that okaayy


lines = readlines()
structs = parse_structs(lines[:30])
print(structs)
dimss, typess = parse_trees(lines[30:])

# actual idiot test data :joy:
print(idiot_solve(dimss, typess))
print(idiot_solve2(dimss, typess, structs))
