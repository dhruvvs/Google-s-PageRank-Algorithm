# DHRUV PATEL 0673
import random

random.seed(0)
N, M = 100, 500
E = set()
while len(E) < M:
    u, v = random.randrange(N), random.randrange(N)
    if u != v:
        E.add((u, v))

with open("biggraph.txt", "w") as f:
    f.write(f"{N} {M}\n")
    for u, v in E:
        f.write(f"{u} {v}\n")
