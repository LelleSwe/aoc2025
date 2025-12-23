def readlines():
    lines = []
    try:
        while (x := input().strip()):
            lines.append(x)
    except:
        pass
    return lines

def parse_lines(lines):
    out = []
    for line in lines:
        w = tuple(map(int, line.split(",")))
        out.append(w)
    return out

points = parse_lines(readlines())
# assert len(points) == 20
# print(len(points))

# class component:
#     def __init__(self):
#         self.state = set()
#
#     def __add__(self, other):
#         self.state.add(other)

def dist(a):
    diff = lambda x, y: (x - y)**2
    return lambda b: sum(map(diff, zip(a, b)))

def dist2(a, b):
    assert len(a) == len(b) == 3
    diff = lambda xy: (xy[0] - xy[1])**2
    return sum(map(diff, zip(a, b)))

def len_sort(p, ps):
    return sorted(ps, key=dist(p))[1:]

components = [set([p]) for p in points]

def merge_component(a, b):
    assert a in components
    assert b in components
    components.remove(a)
    components.remove(b)
    assert a not in components
    assert b not in components
    components.append(a | b)

def gen_lens(points):
    ret = {} 
    skipped = 0
    for i, p1 in enumerate(points):
        for p2 in points:#[i+1:]:
            if p1 == p2:
                skipped += 1
                continue
            if (p2, p1) in ret:
                skipped += 1
                continue
            ret[(p1, p2)] = dist2(p1, p2)

    print(f"skipped {skipped}")
    return ret.items()

points_lens = gen_lens(points)
assert len(points_lens) == len(points) * (len(points) - 1) // 2, len(points_lens)
len_sort2 = lambda xs: sorted(xs, key=lambda x: x[1])
alls = len_sort2(points_lens)
# print("\n".join(map(str, alls)))
alls = iter(alls)

def find_component(p):
    for comp in components:
        if p in comp:
            return comp

while len(components) > 1:
    (p1, p2), _ = next(alls)
    c1 = find_component(p1)
    c2 = find_component(p2)
    if c1 != c2:
        merge_component(c1, c2)

print(p1[0] * p2[0])

# size_sorted = sorted(components, key=lambda x: -len(x))
# # print(size_sorted)
#
# jag_ar_so_lost = list(map(lambda x: len(x), size_sorted))
# print(jag_ar_so_lost[0] * jag_ar_so_lost[1] * jag_ar_so_lost[2])
