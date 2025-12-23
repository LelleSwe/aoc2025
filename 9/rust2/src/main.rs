use bitvector::*;
use itertools::Itertools;
use std::collections::HashSet;
use std::collections::VecDeque;
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

struct Bvec(Vec<BitVector>);

impl Bvec {
    fn new() -> Bvec {
        let mut ret: Vec<BitVector> = Vec::with_capacity(100_101);
        for _ in 0..100_101 {
            ret.push(BitVector::new(100_101));
        }
        Bvec(ret)
    }

    fn set(&mut self, p: (i64, i64)) {
        self.0[p.0 as usize].insert(p.1 as usize);
    }

    fn get(&self, p: (i64, i64)) -> bool {
        self.0[p.0 as usize].contains(p.1 as usize)
    }
}

fn make_boundary(points: &Vec<(i64, i64)>) -> Bvec {
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

    let mut ret = Bvec::new();
    for (p1, p2) in zip(points, points.clone().split_off(1)) {
        let mut p = *p1;
        let dir = mkdir(*p1, p2);
        // print(p1, p2)
        while p != p2 {
            // print(p)
            if ret.get(p) {
                println!("has cycle!"); // test data doesn't cross back on itself!
            }
            ret.set(p);
            p = (p.0 + dir.0, p.1 + dir.1)
            // ret.add(p2)
        }
    }

    let p2 = points[0];
    let mut p = points[points.len() - 1];
    let dir = mkdir(p, p2);
    while p != p2 {
        if ret.get(p) {
            println!("has cycle!");
        }
        ret.set(p);
        p = (p.0 + dir.0, p.1 + dir.1)
        // ret.add(p2)
    }
    return ret;
}

// det här funkar faktiskt :joy: :joy: :joy: :joy: :joy:
fn fill(bound: &mut Bvec, p: (u32, u32)) {
    // let mut counter: u64 = 0;
    // dock holy hell stack-approach exploderade efter counter ~ 400_000_000 med 1_000_000_000
    // element
    // men kön kom bara upp i ~ 370_000 element efter 7_000_000_000 iterationer
    let mut todo = VecDeque::from([p]);
    while todo.len() != 0 {
        let p = todo.pop_front().unwrap();
        if !bound.get((p.0 as i64, p.1 as i64)) {
            bound.set((p.0 as i64, p.1 as i64));
            todo.push_back((p.0 + 1, p.1));
            todo.push_back((p.0 - 1, p.1));
            todo.push_back((p.0, p.1 + 1));
            todo.push_back((p.0, p.1 - 1));
            // counter += 1;
        }
        // if (counter & 0xFFFFFF) == 0 {
        //     println!("{} {}", counter, todo.len());
        // }
    }
}

fn boundary_tostr(
    bound: &Bvec,
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
            } else if bound.get((x, y)) {
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
    bound: &Bvec,
    p1: (i64, i64),
    p2: (i64, i64),
    new_bound: &mut HashSet<(i64, i64)>,
) -> bool {
    let mut p = p1;
    while p != (p2.0 + 1, p2.1) {
        if BOUNDARY {
            new_bound.insert(p);
        }

        if !bound.get(p) {
            return false;
        }

        p = (p.0 + 1, p.1);
    }
    true
}

fn walk_up(
    bound: &Bvec,
    p1: (i64, i64),
    p2: (i64, i64),
    new_bound: &mut HashSet<(i64, i64)>,
) -> bool {
    let mut p = p1;
    while p != (p2.0, p2.1 - 1) {
        if BOUNDARY {
            new_bound.insert(p);
        }

        if !bound.get(p) {
            return false;
        }

        p = (p.0, p.1 - 1);
    }
    true
}

fn valid(
    bound: &Bvec,
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
        return walk_right(bound, p1, p2, new_bound);
    }

    let bl = (p1.0, i64::max(p1.1, p2.1));
    let tr = (p2.0, i64::min(p1.1, p2.1));
    let br = (p2.0, i64::max(p1.1, p2.1));
    let tl = (p1.0, i64::min(p1.1, p2.1));

    if BOUNDARY {
        println!(
            "bl: {} tr: {} br: {} tl: {}",
            ptstr(bl),
            ptstr(tr),
            ptstr(br),
            ptstr(tl)
        );
    }

    return walk_right(bound, bl, br, new_bound)
        && walk_up(bound, br, tr, new_bound)
        && walk_up(bound, bl, tl, new_bound)
        && walk_right(bound, tl, tr, new_bound);
}

fn point_brute(bound: &Bvec, points: Vec<(i64, i64)>) -> i64 {
    let mut marea = 0;

    for (p1, p2) in points.clone().iter().cartesian_product(points) {
        let mut new_bound = HashSet::new();
        if BOUNDARY {
            println!("trying ({}, {}) ({}, {})", p1.0, p1.1, p2.0, p2.1);
        }
        if valid(bound, *p1, p2, &mut new_bound) {
            if BOUNDARY {
                println!(
                    "({}, {}) ({}, {}) is valid (area {})",
                    p1.0,
                    p1.1,
                    p2.0,
                    p2.1,
                    area(*p1, p2)
                );
            }
            if area(*p1, p2) > marea {
                if area(*p1, p2) >= 3113043304 {
                    println!("Too high! ({}, {}) ({}, {})", p1.0, p1.1, p2.0, p2.1);
                }
                if BOUNDARY {
                    println!(
                        "{} ({}, {}) ({}, {})",
                        area(*p1, p2),
                        p1.0,
                        p1.1,
                        p2.0,
                        p2.1
                    );
                }
                marea = area(*p1, p2)
            }
        }
        if BOUNDARY {
            println!("{}", boundary_tostr(bound, &new_bound, *p1, p2, 12, 12));
        }
    }

    marea
}

static BOUNDARY: bool = false;

fn main() {
    let inp = read_lines_one::<String>(496);
    // let inp = read_lines_one::<String>(8);
    // println!("read lines");
    let points = inp
        .iter()
        .filter(|&e| e.len() > 0)
        .map(|e| to_point(e))
        .collect::<Vec<(i64, i64)>>();
    let mut bounds = make_boundary(&points);
    // println!("stack overflow?");
    // eftersom det fungerade så måste denna punkten ha legat innanför boundet :shrug:
    fill(&mut bounds, (98020, 51000));
    // println!("stack overflow? 2");
    if BOUNDARY {
        println!(
            "{}",
            boundary_tostr(&bounds, &HashSet::new(), (0, 0), (0, 0), 12, 12)
        );
    }
    println!("{}", point_brute(&bounds, points));
}
