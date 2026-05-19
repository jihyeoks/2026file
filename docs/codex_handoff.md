# Codex Handoff

## Project

This repository is for a Jupyter notebook simulation of photon-subtracted continuous-variable graph states, based mainly on:

- Mattia Walschaers et al., "Tailoring Non-Gaussian Continuous-Variable Graph States", Phys. Rev. Lett. 121, 220501 (2018).
- Additional reference: `PhysRevA.96.053835.pdf`.

The goal is to reproduce the simulation logic step by step, not to rush into a full implementation.

## Main Working File

- `simul.ipynb`

The notebook should remain the main research record. A `main.py` file is not needed at the current stage.

## Reference PDFs

Local reference paths used on the original machine:

```text
/Users/jujoun/Desktop/!photon subtraction 관련/Reference/교수님의 권유/Phys Rev Lett 2018 Walschaers.pdf
/Users/jujoun/Desktop/!photon subtraction 관련/Reference/교수님의 권유/PhysRevA.96.053835.pdf
```

If working on another computer, copy or relink these papers as needed.

## User Preferences

- Do not jump directly into full coding.
- Discuss/design the notebook structure step by step first.
- Do not create extra notes files unless explicitly requested.
- Keep `README.md` short and command-focused.
- Prefer `simul.ipynb` as the main place for exploratory implementation and verification.
- Use Python modules only later, after notebook functions become stable.

## Current Conceptual Plan

The planned simulation flow is:

```text
adjacency matrix Adj
    -> graph visualization
    -> initial Gaussian covariance V0
    -> CV CZ symplectic matrix G
    -> graph-state covariance V = G V0 G.T
    -> sanity checks
    -> photon subtraction mode f_sub and paper vector g_sub
    -> node-wise observables
    -> graph color plot
```

## Notebook Layer Plan

Use this layer order in `simul.ipynb`:

```text
0. Convention & Goal
1. Input Layer
2. Graph Layer
3. Gaussian Graph-State Layer
4. Sanity Check Layer
5. Photon Subtraction Layer
6. Observable Layer
7. Plot Layer
8. Test Examples
```

Current implementation priority is only:

```text
1. Input Layer
2. Graph Layer
3. Gaussian Graph-State Layer
4. Sanity Check Layer
```

Photon subtraction and excess kurtosis should come after the Gaussian graph-state construction is verified.

## Mathematical Convention

Quadrature ordering:

```text
(q1, q2, ..., qm, p1, p2, ..., pm)
```

Vacuum variance convention for reproducing the Walschaers/PRA formulas directly:

```text
Var(q_vac) = Var(p_vac) = 1
```

Use 0-based indexing internally in Python. Use 1-based labels only for display if helpful.

## Data Separation

Keep these objects conceptually separate:

```text
Adj   : graph adjacency matrix / CZ topology
G     : CV CZ symplectic matrix
G_nx  : optional NetworkX graph object for drawing and graph distances only
V0    : initial Gaussian covariance matrix
V     : graph-state covariance matrix
f_sub : complex subtraction-mode vector, user-facing
g_sub : real phase-space subtraction vector, paper convention
```

Do not store the quantum state in the NetworkX graph.

## Gaussian Graph-State Construction

For the CV CZ graph-state transformation:

```text
q_i -> q_i
p_i -> p_i + sum_j Adj_ij q_j
```

With ordering `(q1,...,qm,p1,...,pm)`, use:

```text
G = [[I,   0],
     [Adj, I]]
```

Then:

```text
V = G @ V0 @ G.T
```

For pure p-squeezed input in the paper convention:

```text
V0 = diag(e^(2r) I, e^(-2r) I)
```

For 10 dB squeezing:

```text
e^(-2r) = 0.1
e^(2r)  = 10
```

So:

```text
V0 = diag(10 I, 0.1 I)
```

## Sanity Checks

Current preference for `Graph-State Sanity` is a light dimension/shape check, not a full physical verification yet.

First verify that the main objects are consistent when `m` or the graph changes:

```text
m is inferred from Adj
Adj has shape m x m
G has shape 2m x 2m
V0 has shape 2m x 2m
V has shape 2m x 2m
f_sub has length m
g_sub has length 2m
Jg_sub has length 2m
Pi_g has shape 2m x 2m
```

This is especially useful because `f_sub` may be hard-coded at first; if the graph size changes, the check should catch dimension mismatches immediately.

Full physics checks can come later, after the notebook structure is stable:

```text
V is symmetric
V is physical
G is symplectic
nullifier variance is correct
```

Graph-state nullifier for the later physical check:

```text
delta_i = p_i - sum_j Adj_ij q_j
```

For 10 dB p-squeezing with vacuum variance `1`, expected nullifier variance:

```text
0.1
```

## Photon Subtraction Plan

Do this later, after the Gaussian part is verified.

Use a complex user-facing subtraction mode vector first:

```text
f_sub in C^m
sum_j |f_sub_j|^2 = 1
```

Then convert it to the paper-convention real phase-space vector:

```text
g_sub = (Re f_sub_1, ..., Re f_sub_m, -Im f_sub_1, ..., -Im f_sub_m)^T
g_sub in R^(2m)
```

Single-vertex subtraction is the special case `f_sub = e_c`.

The photon-subtracted state is non-Gaussian, so covariance alone is insufficient. Use analytic Wigner or characteristic-function formulas from the reference papers.

## First Observable

First target observable:

```text
node-wise phase-quadrature excess kurtosis
```

For node `k`:

```text
K_ex(k) = <(Delta p_k)^4> / <(Delta p_k)^2>^2 - 3
```

Gaussian reference:

```text
K_ex = 0
```

Negative values indicate sub-Gaussian phase-quadrature statistics.

Later:

```text
purity ratio mu / mu_Gauss
single-mode Wigner function W_k(q,p)
```

## Test Graph Order

Start from small graphs:

```text
1. 3-node line graph
2. 7-node line graph
3. small paper-like graph
4. triangular lattice / Fig. 3-like graph
```

Do not start directly from the triangular lattice.

## Recommended Interaction Style

When continuing this project with Codex:

```text
First read docs/codex_handoff.md.
Then inspect simul.ipynb.
Do not immediately implement the full simulation.
Help design or implement only the next small layer.
```
