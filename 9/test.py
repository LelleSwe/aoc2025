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
    return (p1[0] - p2[0] + 1) * (p1[1] - p2[1] + 1)

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


