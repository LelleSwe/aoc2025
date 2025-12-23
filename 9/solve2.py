# this became a bit too complicated for my inexperienced haskell brain lol
from itertools import product
from tqdm import tqdm

def readlines():
    lines = []
    try:
        while (x := input().strip()):
            lines.append(x)
    except:
        pass
    return lines

def to_point(s):
    return tuple(map(int, s.split(",")))

def area(p1, p2):
    return (abs(p1[0] - p2[0]) + 1) * (abs(p1[1] - p2[1]) + 1)

def make_boundary(points):
    def mkdir(p1, p2):
        dir = [p2[0] - p1[0], p2[1] - p1[1]]
        if dir[0] != 0:
            dir[0] = dir[0] // abs(dir[0])
        if dir[1] != 0:
            dir[1] = dir[1] // abs(dir[1])
        dir = tuple(dir)
        return dir

    ret = set()
    for p1, p2 in zip(points, points[1:]):
        p = p1
        dir = mkdir(p1, p2)
        # print(p1, p2)
        while p != p2:
            # print(p)
            if p in ret:
                print("has cycle!") # test data doesn't cross back on itself!
            ret.add(p)
            p = (p[0] + dir[0], p[1] + dir[1])
        # ret.add(p2)

    p2 = points[0]
    p = points[-1]
    dir = mkdir(p, p2)
    while p != p2:
        if p in ret:
            print("has cycle!") 
        ret.add(p)
        p = (p[0] + dir[0], p[1] + dir[1])
    # ret.add(p2)
    return ret

def boundary_tostr(bound, xm, ym):
    out = ""
    for x in range(xm):
        for y in range(ym):
            if (x,y) in bound:
                out += "#"
            else:
                out += "."
        out += "\n"
    return out

# def find_border(bound, p, xm, ym):
#     def top_walk(x, y):
#         while True:
#             if (x,y) in bound:
#                 return False
#             if y >= ym:
#                 return True
#             y += 1
#
#     pass # will have to return to this
#
def walk_right(bound, p1, p2, top, new_bound = None):
    turn_right = lambda xy: ((xy[0], xy[1]) in bound) and ((xy[0], xy[1] - 1) in bound) and ((xy[0], xy[1] + 1) not in bound)
    turn_left  = lambda xy: ((xy[0], xy[1]) in bound) and ((xy[0], xy[1] - 1) not in bound) and ((xy[0], xy[1] + 1) in bound)
    border     = lambda xy: ((xy[0] - 1, xy[1]) not in bound) and ((xy[0], xy[1]) in bound) and ((xy[0], xy[1] + 1) in bound) and ((xy[0], xy[1] - 1) in bound) and ((xy[0] + 1, xy[1]) not in bound)
    p = p1
    while p != (p2[0] + 1, p2[1]):
        if new_bound is not None:
            new_bound.add(p)

        if border(p):
            return False

        if top > 0:
            if turn_right(p):
                return False
            p = (p[0] + 1, p[1])
        elif top < 0:
            if turn_left(p):
                return False
            p = (p[0] + 1, p[1])
        else:
            if p not in bound:
                return False
            p = (p[0] + 1, p[1])
    return True

def walk_up(bound, p1, p2, left, new_bound = None):
    # hoping there aren't 2 lines next to each other
    turn_right = lambda xy: ((xy[0], xy[1]) in bound) and ((xy[0] + 1, xy[1]) not in bound) and ((xy[0] - 1, xy[1]) in bound)
    turn_left  = lambda xy: ((xy[0], xy[1]) in bound) and ((xy[0] + 1, xy[1]) in bound) and ((xy[0] - 1, xy[1]) not in bound)
    # hoping p1 or p2 isn't on a line
    border     = lambda xy: ((xy[0], xy[1] - 1) not in bound) and ((xy[0], xy[1]) in bound) and ((xy[0] + 1, xy[1]) in bound) and ((xy[0] - 1, xy[1]) in bound) and ((xy[0], xy[1] + 1) not in bound)
    p = p1
    while p != (p2[0], p2[1] + 1):
        if new_bound is not None:
            new_bound.add(p)

        if border(p):
            return False

        if left > 0:
            if turn_right(p):
                return False
            p = (p[0], p[1] + 1)
        elif left < 0:
            if turn_left(p):
                return False
            p = (p[0], p[1] + 1)
        else:
            if p not in bound:
                return False
            p = (p[0], p[1] + 1)
    return True

def valid(bound, p1, p2, new_bound = None):
    
    if p1[0] > p2[0]:
        p1, p2 = p2, p1

    top = p1[1] - p2[1]
    if top == 0:
        return walk_right(bound, p1, p2, top, new_bound)

    bl = (p1[0], min(p1[1], p2[1]))
    tr = (p2[0], max(p1[1], p2[1]))
    br = (p2[0], min(p1[1], p2[1]))
    tl = (p1[0], max(p1[1], p2[1]))
    
    return (walk_right(bound, bl, br, -1, new_bound) 
        and walk_up(bound, br, tr, -1, new_bound) 
        and walk_up(bound, bl, tl, 1, new_bound) 
        and walk_right(bound, tl, tr, 1, new_bound))


def point_brute(bound, points):
    marea = 0
    for p1, p2 in tqdm(product(points, repeat=2), total=496**2):
        new_bound = None#set()
        # print(f"trying {p1} {p2}")
        if area(p1, p2) > marea:
            # print(f"{p1} {p2} is valid")
            if valid(bound, p1, p2, new_bound):
                if area(p1, p2) >= 3113043304:
                    print(f"Too high! {p1} {p2}")
                elif area(p1, p2) == 93043:
                    print(f"wrong idk {p1} {p2}")
                print(area(p1, p2), p1, p2)
                marea = area(p1, p2)
        if new_bound is not None:
            print(boundary_tostr(new_bound, 15, 15))

    # # print(f"trying {points[0]} {points[-1]}")
    # if valid(bound, points[0], points[-1]):
    #     # print(f"{points[0]} {points[-1]} is valid")
    #     if area(points[0], points[-1]) > marea:
    #         marea = area(points[0], points[-1])
    return marea

inp = readlines()
points = list(map(to_point, inp))
# print(len(points))
# exit()
bounds = make_boundary(points)
# print(boundary_tostr(bounds, 15, 15), end="")
print(point_brute(bounds, points))
