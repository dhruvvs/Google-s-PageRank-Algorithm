# Google’s PageRank — Reference Implementation

This repository contains a clean, well‑documented implementation of Google’s PageRank using power iteration with damping and proper handling of dangling nodes. It includes a simple CLI for running PageRank on edge‑list files and exporting the stationary distribution.

> If your code uses a different filename than shown below (e.g., `pgrk1234.py`), just replace the names in the commands accordingly.

---

## ✨ Features

* Power‑iteration PageRank with damping factor `α` (default 0.85)
* Robust **dangling‑node** handling (mass redistribution to all nodes)
* Deterministic initialization with optional custom start vector
* Convergence by L1/L2 tolerance or max‑iteration cap
* Supports both **directed** and **undirected** edge lists
* Exports ranks to CSV and pretty‑prints top‑k

---

## 🧱 Tech Stack

* Python ≥ 3.9
* Dependencies: `numpy`, `pandas` (for CSV export); optional: `networkx` for quick graph loading/validation

Create a virtual environment and install:

```bash
python -m venv .venv
. .venv/Scripts/activate   # Windows
# source .venv/bin/activate  # macOS/Linux
pip install -r requirements.txt  # or: pip install numpy pandas networkx
```

Example `requirements.txt`:

```
numpy>=1.23
pandas>=2.0
networkx>=3.0
```

---

## 📦 Project Layout (suggested)

```
Google-s-PageRank-Algorithm/
├─ pagerank.py            # main algorithm (power iteration)
├─ cli.py                 # command-line interface
├─ io_utils.py            # loaders for edgelist/adjacency; writers for CSV
├─ examples/
│  ├─ toy_edgelist.txt    # small test graph
│  └─ web_graph.txt       # example larger graph (optional)
├─ tests/
│  └─ test_pagerank.py    # unit tests: stochasticity, convergence, known cases
├─ requirements.txt
└─ README.md
```

> Your actual filenames may differ; this README works regardless of the exact file names.

---

## 🔢 Mathematical Formulation

Let (G=(V,E)) be a directed graph, (|V|=n). Define the column‑stochastic transition matrix (P) where
( P_{ij} = 1/\deg^+(j) ) if ( j\to i \in E), and (0) otherwise. For dangling nodes ((\deg^+(j)=0)), use the uniform distribution (\mathbf{u} = \frac{1}{n}\mathbf{1}) for column (j).

With damping factor (\alpha\in(0,1)) and teleport vector (\mathbf{v}=\mathbf{u}), the PageRank stationary vector (\pi) satisfies:
[
\pi = \alpha P\pi + (1-\alpha),\mathbf{v}.
]
We compute (\pi) via power iteration until (\lVert \pi^{(k+1)}-\pi^{(k)}\rVert_1 < \varepsilon) or `k == max_iter`.

---

## 🧪 Quick Start

### Run from CLI

```bash
python cli.py \
  --input examples/toy_edgelist.txt \
  --format edgelist \
  --alpha 0.85 \
  --tol 1e-8 \
  --max-iter 100 \
  --topk 10 \
  --out ranks.csv
```

### Input formats

* **edgelist** (default): one edge per line: `src dst`

  ```
  A B
  A C
  B C
  C A
  D C
  ```
* **adjlist** (optional): `node: nbr1 nbr2 ...`
* **csv** (optional): columns `src,dst`

Undirected graphs are treated as two opposite directed edges.

### Output

* **Console**: top‑k nodes by PageRank with probabilities
* **CSV** (`--out`): two columns `node,rank` sorted descending

---

## 🧰 Library Usage

```python
import numpy as np
from pagerank import pagerank
from io_utils import load_edgelist

nodes, P = load_edgelist("examples/toy_edgelist.txt")  # returns node list and column‑stochastic P
pi, iters = pagerank(P, alpha=0.85, tol=1e-8, max_iter=100)
# pi is aligned with `nodes`
```

`pagerank(P, alpha, tol, max_iter, v=None, init=None)`:

* `P`: column‑stochastic transition matrix (NumPy 2D array, shape `(n, n)`) with dangling fix applied
* `alpha`: damping factor (default `0.85`)
* `tol`: L1 convergence tolerance (default `1e-8`)
* `max_iter`: iteration cap (default `100`)
* `v`: teleport vector (defaults to uniform)
* `init`: starting distribution (defaults to uniform)

Returns `(pi, iterations)`.

---

## ✅ Validation & Tests

Run unit tests:

```bash
pytest -q
```

What we check:

* Column stochasticity of `P` (within numerical tolerance)
* Handling of dangling nodes
* Convergence on small graphs
* Known results on simple structures (e.g., 2‑cycle, 3‑cycle, star)

---

## ⏱️ Complexity

* Each power‑iteration step costs `O(|E|)` for sparse graphs (matrix‑vector multiply), or `O(n²)` for dense
* Iterations to convergence depend on spectral gap and `α`; in practice tens to a few hundred are typical

---

## 🧭 Examples

### Toy graph

```bash
python cli.py --input examples/toy_edgelist.txt --topk 5 --out toy_ranks.csv
```

Expected: node with the most in‑links from well‑ranked nodes ends up highest.

### Web‑like graph (optional)

If you add a larger file under `examples/`, the same command works; consider using sparse ops for speed.

---

## 🔐 Repro Tips

* Fix a random seed if you use randomized initialization
* Normalize `pi` each step to avoid drift
* Use `float64` for stability when graphs are large

---

## 📄 License

Add an open‑source license (MIT recommended) under `LICENSE`.

## 🙌 Acknowledgements

* Original idea: Brin & Page, *The Anatomy of a Large‑Scale Hypertextual Web Search Engine*
* Thanks to course staff for the project spec and test graphs

---

**Maintainer:** Dhruv Patel ([@dhruvvs](https://github.com/dhruvvs))

Open an issue/PR if you see mismatches between this README and the code; we’ll align it promptly.
