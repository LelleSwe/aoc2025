use itertools::Itertools;
use std::collections::HashSet;
use std::io;
use std::iter::zip;
use std::str;

pub fn read_lines_one<T: str::FromStr>(amount: usize) -> Vec<T> {
    let mut buffer = String::new();
    for _ in 0..amount {
        let _ = io::Stdin::read_line(&io::stdin(), &mut buffer);
    }
    buffer
        .split('\n')
        .filter_map(|s| s.trim().parse().ok())
        .collect()
}

fn to_point(s: &String) -> (i64, i64) {
    let ab = s.split(",").collect::<Vec<&str>>();
    if ab.len() != 2 {
        println!("{:#?}", ab);
    }
    let a = ab[0];
    let b = ab[1];
    (a.parse::<i64>().unwrap(), b.parse::<i64>().unwrap())
}

fn area(p1: (i64, i64), p2: (i64, i64)) -> i64 {
    ((p1.0 - p2.0).abs() + 1) * ((p1.1 - p2.1).abs() + 1)
}

fn make_boundary(points: &Vec<(i64, i64)>) -> HashSet<(i64, i64)> {
    fn mkdir(p1: (i64, i64), p2: (i64, i64)) -> (i64, i64) {
        let mut dir: (i64, i64) = (p2.0 - p1.0, p2.1 - p1.1);
        if dir.0 != 0 {
            dir.0 = dir.0 / dir.0.abs();
        }
        if dir.1 != 0 {
            dir.1 = dir.1 / dir.1.abs();
        }
        return dir;
    }

    let mut ret = HashSet::new();
    for (p1, p2) in zip(points, points.clone().split_off(1)) {
        let mut p = *p1;
        let dir = mkdir(*p1, p2);
        // print(p1, p2)
        while p != p2 {
            // print(p)
            if ret.contains(&p) {
                println!("has cycle!"); // test data doesn't cross back on itself!
            }
            ret.insert(p);
            p = (p.0 + dir.0, p.1 + dir.1)
            // ret.add(p2)
        }
    }

    let p2 = points[0];
    let mut p = points[points.len() - 1];
    let dir = mkdir(p, p2);
    while p != p2 {
        if ret.contains(&p) {
            println!("has cycle!");
        }
        ret.insert(p);
        p = (p.0 + dir.0, p.1 + dir.1)
        // ret.add(p2)
    }
    return ret;
}

fn boundary_tostr(
    bound: &HashSet<(i64, i64)>,
    new_bound: &HashSet<(i64, i64)>,
    p1: (i64, i64),
    p2: (i64, i64),
    xm: i64,
    ym: i64,
) -> String {
    let mut out = String::new();
    for y in 0..ym {
        for x in 0..xm {
            if (x, y) == p1 {
                out += "1"
            } else if (x, y) == p2 {
                out += "2"
            } else if new_bound.contains(&(x, y)) {
                out += "O"
            } else if bound.contains(&(x, y)) {
                out += "#"
            } else {
                out += "."
            }
        }
        out += "\n"
    }
    out
}

fn ptstr(p: (i64, i64)) -> String {
    format!("({}, {})", p.0, p.1)
}

fn walk_right(
    bound: &mut HashSet<(i64, i64)>,
    p1: (i64, i64),
    p2: (i64, i64),
    top: i64,
    new_bound: &mut HashSet<(i64, i64)>,
) -> bool {
    let turn_right = |(x, y)| {
        bound.contains(&(x, y))
            && !bound.contains(&(x, y - 1))
            && bound.contains(&(x, y + 1))
            && bound.contains(&(x - 1, y))
            && (x, y) != p1
            && (x, y) != p2
    };
    let turn_left = |(x, y)| {
        bound.contains(&(x, y))
            && bound.contains(&(x, y - 1))
            && !bound.contains(&(x, y + 1))
            && bound.contains(&(x - 1, y))
            && (x, y) != p1
            && (x, y) != p2
    };
    /*
     * this border function has edge cases:
     * ....#.....................#...
     * ....1.....................2...
     * ....#.....................#...
     */
    // let border = |(x, y)| {
    //     !bound.contains(&(x - 1, y))
    //         && bound.contains(&(x, y))
    //         && bound.contains(&(x, y + 1))
    //         && bound.contains(&(x, y - 1))
    //         && !bound.contains(&(x + 1, y))
    // };
    let mut p = p1;
    while p != (p2.0 + 1, p2.1) {
        if BOUNDARY {
            new_bound.insert(p);
        }

        // if border(p) {
        //     return false;
        // }

        if top > 0 {
            if turn_right(p) {
                println!("failed turn_right, walk_right, {}", ptstr(p));
                return false;
            }
        } else if top < 0 {
            if turn_left(p) {
                println!("failed turn_left, walk_right, {}", ptstr(p));
                return false;
            }
        } else {
            /*
             * this can still shit itself:
             * ...........................
             * ....1#########.....#####2..
             * .............#.....#.......
             * .............#######.......
             * ...........................
             */
            if !bound.contains(&p) {
                println!("failed else, walk_right, {}", ptstr(p));
                return false;
            }
        }
        p = (p.0 + 1, p.1);
    }
    true
}

fn walk_up(
    bound: &mut HashSet<(i64, i64)>,
    p1: (i64, i64),
    p2: (i64, i64),
    left: i64,
    new_bound: &mut HashSet<(i64, i64)>,
) -> bool {
    // # hoping there aren't 2 lines next to each other
    let turn_right = |(x, y)| {
        bound.contains(&(x, y))
            && bound.contains(&(x + 1, y))
            && !bound.contains(&(x - 1, y))
            && bound.contains(&(x, y + 1))
            && (x, y) != p1
            && (x, y) != p2
    };
    let turn_left = |(x, y)| {
        bound.contains(&(x, y))
            && !bound.contains(&(x + 1, y))
            && bound.contains(&(x - 1, y))
            && bound.contains(&(x, y + 1))
            && (x, y) != p1
            && (x, y) != p2
    };
    // # hoping p1 or p2 isn't on a line
    // let border = |(x, y)| {
    //     !bound.contains(&(x, y - 1))
    //         && bound.contains(&(x, y))
    //         && bound.contains(&(x + 1, y))
    //         && bound.contains(&(x + 1, y))
    //         && !bound.contains(&(x, y + 1))
    // };

    let mut p = p1;
    assert!(p.1 >= p2.1);
    while p != (p2.0, p2.1 - 1) {
        println!("{}", ptstr(p));
        if BOUNDARY {
            new_bound.insert(p);
        }

        // if border(p) {
        //     return false;
        // }

        if left > 0 {
            if turn_right(p) {
                println!("failed turn_right, walk_up, {}", ptstr(p));
                return false;
            }
            p = (p.0, p.1 - 1);
        } else if left < 0 {
            if turn_left(p) {
                println!("failed turn_left, walk_up, {}", ptstr(p));
                return false;
            }
            p = (p.0, p.1 - 1);
        } else {
            if !bound.contains(&p) {
                println!("failed else, walk_up, {}", ptstr(p));
                return false;
            }
            p = (p.0, p.1 - 1);
        }
    }
    true
}

fn valid(
    bound: &mut HashSet<(i64, i64)>,
    p1: (i64, i64),
    p2: (i64, i64),
    new_bound: &mut HashSet<(i64, i64)>,
) -> bool {
    let (mut p1, mut p2) = (p1, p2);
    if p1.0 > p2.0 {
        (p1, p2) = (p2, p1);
    }
    assert!(p1.0 <= p2.0);

    let top = p1.1 - p2.1;
    if top == 0 {
        return walk_right(bound, p1, p2, top, new_bound);
    }

    let bl = (p1.0, i64::max(p1.1, p2.1));
    let tr = (p2.0, i64::min(p1.1, p2.1));
    let br = (p2.0, i64::max(p1.1, p2.1));
    let tl = (p1.0, i64::min(p1.1, p2.1));

    println!(
        "bl: {} tr: {} br: {} tl: {}",
        ptstr(bl),
        ptstr(tr),
        ptstr(br),
        ptstr(tl)
    );

    return walk_right(bound, bl, br, -1, new_bound)
        && walk_up(bound, br, tr, -1, new_bound)
        && walk_up(bound, bl, tl, 1, new_bound)
        && walk_right(bound, tl, tr, 1, new_bound);
}

fn point_brute(bound: &mut HashSet<(i64, i64)>, points: Vec<(i64, i64)>) -> i64 {
    let mut marea = 0;

    for (p1, p2) in points.clone().iter().cartesian_product(points) {
        let mut new_bound = HashSet::new();
        println!("trying ({}, {}) ({}, {})", p1.0, p1.1, p2.0, p2.1);
        if valid(bound, *p1, p2, &mut new_bound) {
            println!(
                "({}, {}) ({}, {}) is valid (area {})",
                p1.0,
                p1.1,
                p2.0,
                p2.1,
                area(*p1, p2)
            );
            if area(*p1, p2) > marea {
                if area(*p1, p2) >= 3113043304 {
                    println!("Too high! ({}, {}) ({}, {})", p1.0, p1.1, p2.0, p2.1);
                }
                println!(
                    "{} ({}, {}) ({}, {})",
                    area(*p1, p2),
                    p1.0,
                    p1.1,
                    p2.0,
                    p2.1
                );
                marea = area(*p1, p2)
            }
        }
        if BOUNDARY {
            println!("{}", boundary_tostr(bound, &new_bound, *p1, p2, 12, 12));
        }
    }

    marea
}

static BOUNDARY: bool = true;

fn main() {
    // let inp = read_lines_one::<String>(496);
    let inp = read_lines_one::<String>(8);
    println!("read lines");
    let points = inp
        .iter()
        .filter(|&e| e.len() > 0)
        .map(|e| to_point(e))
        .collect::<Vec<(i64, i64)>>();
    let mut bounds = make_boundary(&points);
    println!(
        "{}",
        boundary_tostr(&bounds, &HashSet::new(), (0, 0), (0, 0), 12, 12)
    );
    println!("{}", point_brute(&mut bounds, points));
}
