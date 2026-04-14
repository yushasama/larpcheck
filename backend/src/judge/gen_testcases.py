#!/usr/bin/env python3
"""
Generates problem_bank/<id>.in for all problems a-l.
15 test cases per problem with realistic contest distribution:
  3 small, 7 medium, 4 large, 1 max

Run gen_expected.sh afterward to produce .out files.

Usage:
    python build_bank.py [--seed N] [--out DIR] [--problems a b ...]
"""

import argparse, heapq, random
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).parent.parent / "ransomware"))
from crypto import make_fernet


# ═══════════════════════════════════════════════════════
# Helpers
# ═══════════════════════════════════════════════════════

def rand_tree(n, rng):
    if n == 1: return []
    if n == 2: return [(1, 2)]
    prufer = [rng.randint(1, n) for _ in range(n - 2)]
    degree = [1] * (n + 1)
    for v in prufer: degree[v] += 1
    heap = [i for i in range(1, n + 1) if degree[i] == 1]
    heapq.heapify(heap)
    edges = []
    for v in prufer:
        u = heapq.heappop(heap)
        edges.append((u, v))
        degree[u] -= 1; degree[v] -= 1
        if degree[v] == 1: heapq.heappush(heap, v)
    last = [i for i in range(1, n + 1) if degree[i] == 1]
    edges.append((last[0], last[1]))
    return edges

def rand_graph(n, m, rng):
    edge_set = {(min(u,v), max(u,v)) for u,v in rand_tree(n, rng)}
    attempts = 0
    while len(edge_set) < m and attempts < m * 10:
        u, v = rng.randint(1, n), rng.randint(1, n)
        if u != v: edge_set.add((min(u,v), max(u,v)))
        attempts += 1
    return [(u, v, rng.randint(1, 10**9)) for u, v in edge_set]

def contest_sizes(lo, hi, rng):
    """
    Returns 15 values with contest distribution:
      3 small  (lo .. lo + (hi-lo)*0.1)
      7 medium (lo + (hi-lo)*0.1 .. lo + (hi-lo)*0.7)
      4 large  (lo + (hi-lo)*0.7 .. hi-1)
      3 max    (hi)
    """
    s = lo + max(1, int((hi - lo) * 0.10))
    m = lo + max(1, int((hi - lo) * 0.70))
    sizes  = [rng.randint(lo, s) for _ in range(3)]
    sizes += [rng.randint(s, m)  for _ in range(6)]
    sizes += [rng.randint(m, hi) for _ in range(3)]
    sizes += [hi, hi, hi]
    rng.shuffle(sizes)
    return sizes


# ═══════════════════════════════════════════════════════
# Generators
# ═══════════════════════════════════════════════════════

def gen_a(rng):
    sizes = contest_sizes(1, 10**4, rng)
    lines = [str(len(sizes))]
    for n in sizes:
        lines.append(str(n))
    return "\n".join(lines)

def gen_b(rng):
    sizes = contest_sizes(1, 10**4, rng)
    lines = [str(len(sizes))]
    for n in sizes:
        arr = sorted(rng.sample(range(-9999, 10000), min(n, 19999)))
        k = rng.choice(arr) if rng.random() < 0.7 else rng.randint(-9999, 9999)
        lines += [f"{len(arr)} {k}", " ".join(map(str, arr))]
    return "\n".join(lines)

def gen_c(rng):
    sizes = contest_sizes(1, 10**4, rng)  # kept smaller so sum stays sane
    lines = [str(len(sizes))]
    for n in sizes:
        q = rng.randint(1, n)
        arr = [rng.randint(1, 10**9) for _ in range(n)]
        lines += [f"{n} {q}", " ".join(map(str, arr))]
        lines += [str(rng.randint(1, n)) for _ in range(q)]
    return "\n".join(lines)

def gen_d(rng):
    sizes = contest_sizes(1, 10**4, rng)
    lines = [str(len(sizes))]
    for n in sizes:
        q = rng.randint(1, n)
        vals = [rng.randint(1, 10**9) for _ in range(n)]
        edges = rand_tree(n, rng)
        lines += [f"{n} {q}", " ".join(map(str, vals))]
        for u, v in edges: lines.append(f"{u} {v}")
        lines += [str(rng.randint(1, n)) for _ in range(q)]
    return "\n".join(lines)

def gen_e(rng):
    # n <= 500, sum <= 2e4 — keep sizes bounded
    sizes = contest_sizes(1, 500, rng)
    lines = [str(len(sizes))]
    for n in sizes:
        lines += [str(n), " ".join(str(rng.randint(1, n)) for _ in range(n))]
    return "\n".join(lines)

def gen_f(rng):
    sizes = contest_sizes(2, 10**4, rng)
    lines = [str(len(sizes))]
    for n in sizes:
        perm = list(range(1, n+1)); rng.shuffle(perm)
        rem = [0] * (n+1)
        idx = 0
        while idx < n:
            left = n - idx
            size = rng.randint(2, min(left, 6)) if left >= 2 else 2
            if left - size == 1: size = left
            circle = perm[idx:idx+size]; idx += size
            for j, p in enumerate(circle):
                rem[p] = rng.choice([circle[(j-1)%size], circle[(j+1)%size]])
        lines += [str(n), " ".join(str(rem[i]) for i in range(1, n+1))]
    return "\n".join(lines)

def gen_g(rng):
    sizes = contest_sizes(2, 10**4, rng)
    lines = [str(len(sizes))]
    for n in sizes:
        m = rng.randint(n-1, min(n*(n-1)//2, n*3))
        B = rng.randint(1, 10**9)
        edges = rand_graph(n, m, rng)
        lines.append(f"{n} {len(edges)} {B}")
        for u, v, c in edges: lines.append(f"{u} {v} {c}")
    return "\n".join(lines)

def gen_h(rng):
    sizes = contest_sizes(1, 10**4, rng)
    lines = [str(len(sizes))]
    for n in sizes:
        q = rng.randint(1, n)
        vals = [rng.randint(1, 10**9) for _ in range(n)]
        edges = rand_tree(n, rng)
        lines += [f"{n} {q}", " ".join(map(str, vals))]
        for u, v in edges: lines.append(f"{u} {v}")
        for _ in range(q):
            if rng.random() < 0.4: lines.append(f"1 {rng.randint(1,n)} {rng.randint(1,10**9)}")
            else: lines.append(f"2 {rng.randint(1,n)}")
    return "\n".join(lines)

def gen_i(rng):
    # n <= 18 hard limit, t <= 10 — 10 cases all at max
    sizes = contest_sizes(1, 18, rng)[:10]  # t <= 10
    lines = [str(len(sizes))]
    for n in sizes:
        lines.append(str(n))
        for _ in range(n):
            lines.append(" ".join(str(rng.randint(0, 10**6)) for _ in range(n)))
    return "\n".join(lines)

def gen_j(rng):
    sizes = contest_sizes(1, 10**4, rng)
    lines = [str(len(sizes))]
    for n in sizes:
        rates = [rng.randint(1, 10**9) for _ in range(n)]
        edges = rand_tree(n, rng)
        lines += [str(n), " ".join(map(str, rates))]
        for u, v in edges: lines.append(f"{u} {v}")
    return "\n".join(lines)

def gen_k(rng):
    sizes = contest_sizes(2, 10**4, rng)
    lines = [str(len(sizes))]
    for n in sizes:
        checks = [rng.randint(-10**9, 10**9) for _ in range(n)]
        i, j = rng.sample(range(n), 2)
        lines += [f"{n} {checks[i]+checks[j]}", " ".join(map(str, checks))]
    return "\n".join(lines)

def gen_l(rng):
    # t <= 10, n <= 3000, O(n^2) solver — 10 cases
    sizes = contest_sizes(3, 3000, rng)[:10]
    lines = [str(len(sizes))]
    for n in sizes:
        fees = rng.sample(range(-10**8, 10**8), n)
        i, j, k = rng.sample(range(n), 3)
        B = fees[i] + fees[j] + fees[k]
        edge_set = set()
        for _ in range(rng.randint(0, min(n*(n-1)//2, n*5))):
            u, v = rng.randint(1,n), rng.randint(1,n)
            if u != v: edge_set.add((min(u,v), max(u,v)))
        lines.append(f"{n} {len(edge_set)} {B}")
        lines.append(" ".join(map(str, fees)))
        for u, v in edge_set: lines.append(f"{u} {v}")
    return "\n".join(lines)


GENERATORS = {
    "a": gen_a, "b": gen_b, "c": gen_c, "d": gen_d,
    "e": gen_e, "f": gen_f, "g": gen_g, "h": gen_h,
    "i": gen_i, "j": gen_j, "k": gen_k, "l": gen_l,
}

def encrypt_outputs(out_dir: Path) -> None:
    f = make_fernet()
    for out_path in out_dir.glob("*.out"):
        enc = f.encrypt(out_path.read_bytes())
        out_path.with_suffix(".out.enc").write_bytes(enc)
        out_path.unlink()
        print(f"  encrypted → {out_path.stem}.out.enc")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed",     type=int,   default=None)
    parser.add_argument("--out",      type=str,   default="../problem_bank/testcases")
    parser.add_argument("--problems", nargs="*",  default=list(GENERATORS.keys()))

    args = parser.parse_args()

    seed = args.seed if args.seed is not None else random.randint(0, 2**31)
    rng  = random.Random(seed)
    out_dir = Path(args.out)
    out_dir.mkdir(parents=True, exist_ok=True)

    print(f"Seed: {seed}")
    for pid in args.problems:
        content = GENERATORS[pid](rng)
        (out_dir / f"{pid}.in").write_text(content)
        T = content.split('\n')[0]
        print(f"  [{pid}] {T} cases → {out_dir}/{pid}.in")
    print("Done. Run gen_expected.sh to produce .out files.")

if __name__ == "__main__":
    main()