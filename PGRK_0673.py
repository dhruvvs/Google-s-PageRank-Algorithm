# DHRUV PATEL 0673
import sys, math

DAMPING = 0.85

def _read_graph(path):
    with open(path, "r", encoding="utf-8") as f:
        # read header "N M"
        for line in f:
            s = line.strip()
            if s:
                a = s.split()
                if len(a) < 2:
                    raise SystemExit("First line must be: N M")
                N, M = int(a[0]), int(a[1])
                break
        else:
            raise SystemExit("Empty graph file.")

        # build adjacency and outdeg
        adj = [[] for _ in range(N)]
        outdeg = [0]*N
        for _ in range(M):
            line = f.readline()
            if not line: break
            s = line.strip()
            if not s: continue
            a = s.split()
            if len(a) < 2: continue
            u, v = int(a[0]), int(a[1])
            if 0 <= u < N and 0 <= v < N:
                adj[u].append(v)
                outdeg[u] += 1

    return N, adj, outdeg

def _init_vec(N, initialvalue):
    if initialvalue == 0:
        x = [0.0]*N
    elif initialvalue == 1:
        x = [1.0]*N
    elif initialvalue == -1:
        val = 1.0/N
        x = [val]*N
    elif initialvalue == -2:
        val = 1.0/math.sqrt(N)
        x = [val]*N
    else:
        x = [1.0/N]*N
    return x

def _l1_scale(x):
    s = sum(x)
    if s != 0.0:
        inv = 1.0/s
        for i in range(len(x)):
            x[i] *= inv

def _print_base(P):
    N = len(P)
    if N <= 10:
        parts = [f"P[{i:2d}]={P[i]:.7f}" for i in range(N)]
        sys.stdout.write("Base : 0 :" + " ".join(parts) + "\n")

def _print_iter(t, P):
    N = len(P)
    if N <= 10:
        parts = [f"P[{i:2d}]={P[i]:.7f}" for i in range(N)]
        sys.stdout.write(f"Iter : {t} :" + " ".join(parts) + "\n")

def pagerank(N, adj, outdeg, iterations, initialvalue):
    # If N>10, per spec: behave like iterations=0 (error-rate default 1e-5)
    if N > 10:
        iterations = 0

    if iterations == 0:
        err = 1e-5
        fixed_iters = None
    elif iterations < 0:
        err = 10.0 ** iterations  # e.g., -3 -> 1e-3
        fixed_iters = None
    else:
        err = None
        fixed_iters = iterations

    P = _init_vec(N, initialvalue)
    _l1_scale(P)

    _print_base(P)

    # locals for speed
    d = DAMPING
    invN = 1.0 / N if N else 0.0
    base_term = (1.0 - d) * invN

    t = 0
    while True:
        t += 1
        newP = [base_term]*N

        # dangling mass (sum of ranks of nodes with outdeg==0)
        dm = 0.0
        for i in range(N):
            if outdeg[i] == 0:
                dm += P[i]

        share_dangling = d * dm * invN

        # distribute rank contributions from non-dangling nodes
        for u in range(N):
            od = outdeg[u]
            if od == 0:
                continue
            contrib = d * (P[u] / od)
            for v in adj[u]:
                newP[v] += contrib

        if dm != 0.0:
            # add redistributed dangling mass uniformly
            add = share_dangling
            for i in range(N):
                newP[i] += add

        # scaling step keeps L1=1 to avoid drift
        _l1_scale(newP)

        if fixed_iters is None:
            # error-rate mode
            if N <= 10:
                _print_iter(t, newP)
            # max absolute diff
            diff = 0.0
            # tight loop: manual max
            for i in range(N):
                di = newP[i] - P[i]
                if di < 0: di = -di
                if di > diff:
                    diff = di
            if diff <= err:
                break
        else:
            # fixed-iteration mode
            _print_iter(t, newP)
            if t >= fixed_iters:
                break

        P = newP

    # final printing for big N
    if N > 10:
        sys.stdout.write(f"Iter : {t}\n")
        for i in range(N):
            sys.stdout.write(f"P[{i:2d}]={newP[i]:.7f}\n")

def main():
    if len(sys.argv) != 4:
        sys.stderr.write("Usage: python pgrk_1234.py <iterations> <initialvalue> <graphfile>\n")
        sys.exit(1)
    iterations = int(sys.argv[1])
    initialvalue = int(sys.argv[2])
    graphfile = sys.argv[3]

    N, adj, outdeg = _read_graph(graphfile)
    pagerank(N, adj, outdeg, iterations, initialvalue)

if __name__ == "__main__":
    main()
