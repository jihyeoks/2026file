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
    -> effective nullifier graph from covariance V
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
   2-1. Given graph structure from Adj
   2-2. Effective Nullifier Graph from Covariance
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

## Graph Layer Details

The current `Graph Layer` should be split into two substeps.

### 2-1. Given Graph Structure from Adj

This is the direct graph check from the user-provided adjacency matrix:

```text
Adj -> graph structure / edge list / graph drawing
```

This step answers:

```text
What graph did we manually put into the notebook?
```

`Adj` is the source of truth for this step. NetworkX may be used as a visualization/helper tool:

```text
Adj -> G_nx -> drawing / edge list / graph distance
```

Here, `G_nx` is only for graph visualization and graph-theoretic utilities. It is not the quantum state, and it is not the CV CZ symplectic matrix `G`.

Recommended package direction:

```text
calculation: numpy
visualization / edge handling / graph distances: NetworkX + matplotlib
```

NetworkX is preferred for now because the graphs are small, the notebook should remain readable, and later distance-from-subtraction-node analysis may be useful.

### 2-2. Effective Nullifier Graph from Covariance

This is the next planned graph-layer method.

Use the section title:

```markdown
## 2. Effective Nullifier Graph from Covariance
```

or, if the notebook needs shorter wording:

```markdown
## 2. Recover Effective Adjacency from V
```

Preferred name for accuracy:

```text
Effective Nullifier Graph from Covariance
```

The goal is:

```text
Given an arbitrary covariance matrix V, estimate a graph-like effective adjacency Gamma_eff.
```

This does not mean that an arbitrary `V` has a unique original CV graph-state adjacency. Instead, it gives the best linear nullifier-style graph relation:

```text
p approximately Gamma_eff x
delta = p - Gamma_eff x
```

With quadrature ordering:

```text
(q1, q2, ..., qm, p1, p2, ..., pm)
```

split `V` into blocks:

```text
V = [[V_xx, V_xp],
     [V_px, V_pp]]
```

Then define:

```text
Gamma_eff = V_px @ pinv(V_xx)
```

This is a least-squares/nullifier fit. It can be applied to an arbitrary physical covariance matrix `V`.

For an ideal graph state:

```text
V = G @ V_in @ G.T
```

where `V_in` has no x-p cross correlations, this method should recover the original adjacency:

```text
Gamma_eff = Adj
```

Thus this step has two uses:

```text
1. Check that the ideal graph-state covariance recovers the manually chosen Adj.
2. For a general covariance V, extract a graph-like effective adjacency for visualization/diagnosis.
```

For plotting, `Gamma_eff` may not be symmetric. Keep the raw matrix for analysis, but use a symmetrized version for undirected graph drawing:

```text
Gamma_plot = (Gamma_eff + Gamma_eff.T) / 2
diag(Gamma_plot) = 0
```

This symmetrization is only for plotting.

Also compute the nullifier covariance for fit quality:

```text
V_delta =
    V_pp
    - Gamma_eff @ V_xp
    - V_px @ Gamma_eff.T
    + Gamma_eff @ V_xx @ Gamma_eff.T
```

Track:

```text
Gamma_eff
Gamma_plot
V_delta
diag(V_delta)
```

If `diag(V_delta)` is small, then the covariance is more graph-state-like in this nullifier sense. If it is large, the plotted graph may still be useful as a correlation/fit visualization, but it should not be interpreted as a recovered physical CZ topology.

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
