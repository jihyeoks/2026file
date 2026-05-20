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

- Absolute editing gate: do not modify files unless the user explicitly says one
  of these exact Korean trigger phrases:
  - `수정해`
  - `파일에 넣어`
  - `노트북에 추가해`
- If the user says anything else, including exploratory phrases like
  `만들어볼까`, `해볼까`, `생각해보자`, or `코드 짜볼까`, do not treat it as
  permission to edit. Ask for confirmation before modifying any file.
- Reading files, explaining, planning, and showing code drafts in chat are okay.
  Writing files, patching files, formatting notebooks, or running commands that
  change files requires one of the exact trigger phrases above.
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

This is the current graph-layer plan.

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

### Goal

```text
Draw a graph from an arbitrary Gaussian covariance matrix V, not only from the
original adjacency matrix Adj.
```

The graph should be an effective nullifier graph: the graph-like relation
between x and p quadratures that makes the nullifier noise smallest.

This is not a Williamson or Bloch-Messiah decomposition. It is a
least-squares fitting problem.

This does not mean that an arbitrary `V` has a unique original CV graph-state
adjacency. Instead, it gives the best linear nullifier-style graph relation.

### Current Convention

Quadrature ordering:

```text
q = (x_1, ..., x_m, p_1, ..., p_m)^T
```

Vacuum variance convention:

```text
V_vac = I
```

The current notebook already defines:

```text
Adj      : original graph adjacency
m        : number of modes
Omega    : [[0, I], [-I, 0]]
J        : Omega.T
G        : graph-state symplectic matrix, paper notation
V0       : input covariance
V        : graph-state covariance, V = G @ V0 @ G.T
```

The paper uses `G` for the graph-state symplectic transformation, so keep the
name `G`.

### Effective Nullifier Graph Algorithm

Given an arbitrary covariance matrix:

```text
V = [[V_xx, V_xp],
     [V_px, V_pp]]
```

consider two possible graph-like nullifier forms:

```text
delta_1 = p - Gamma_1 x
delta_2 = x - Gamma_2 p
```

For each direction, find the best-fit `Gamma` by minimizing the residual noise.

Case 1, `p - Gamma x`:

```text
Gamma_1 = V_px @ pinv(V_xx)
```

Residual covariance:

```text
V_delta_1 =
    V_pp
    - Gamma_1 @ V_xp
    - V_px @ Gamma_1.T
    + Gamma_1 @ V_xx @ Gamma_1.T
```

Case 2, `x - Gamma p`:

```text
Gamma_2 = V_xp @ pinv(V_pp)
```

Residual covariance:

```text
V_delta_2 =
    V_xx
    - Gamma_2 @ V_px
    - V_xp @ Gamma_2.T
    + Gamma_2 @ V_pp @ Gamma_2.T
```

Compare the two directions using:

```text
trace(V_delta_1)
trace(V_delta_2)
```

Choose the direction with smaller trace.

The selected matrix is:

```text
Gamma_eff
```

The selected nullifier covariance is:

```text
V_delta
```

The node-wise nullifier noise is:

```text
nullifier_var = diag(V_delta)
```

Since `V_vac = I`, a node satisfies the squeezed nullifier condition if:

```python
nullifier_var[i] < 1
```

### Important Ideal Graph-State Check

For the ideal graph state currently generated by:

```text
V = G @ V0 @ G.T
G = [[I,   0],
     [Adj, I]]
```

the first direction should win:

```text
delta_1 = p - Gamma_1 x
```

Also:

```text
Gamma_1 approximately equals Adj
```

So the notebook should print:

```python
max |Gamma1 - Adj|
```

This should be close to numerical zero for the current ideal test case.

### Plotting Plan

Use NetworkX only for drawing.

For graph plotting, the fitted `Gamma_eff` may not be symmetric for arbitrary
`V`. Keep the raw matrix for analysis, but make a plotting-only matrix:

```python
Gamma_plot = 0.5 * (Gamma_eff + Gamma_eff.T)
np.fill_diagonal(Gamma_plot, 0)
```

Then threshold small edges:

```python
A_plot = np.where(np.abs(Gamma_plot) > threshold, np.abs(Gamma_plot), 0)
```

Convert to a NetworkX graph:

```python
G_plot = nx.from_numpy_array(A_plot)
```

Use automatic layout:

```python
pos = nx.spring_layout(G_plot, seed=0)
```

or, if the result looks better:

```python
pos = nx.kamada_kawai_layout(G_plot)
```

Node color should represent the quantity to visualize. Start with:

```python
node_values = nullifier_var
```

Later the same plotting function should be reused for:

```python
node_values = kurtosis_values
node_values = purity_ratio
node_values = other node-wise quantities
```

Define a reusable function in the first cell:

```python
plot_graph_from_matrix(W, node_values=None, title="", threshold=1e-6, pos=None)
```

This function should:

```text
1. symmetrize W for plotting
2. zero the diagonal
3. threshold small edges
4. create a NetworkX graph
5. use automatic layout if pos is None
6. draw nodes with node_values as color
7. return pos so later plots can reuse the same layout
```

This allows the same graph shape to be reused when plotting nullifier variance,
kurtosis, purity, and other node-wise quantities.

Core summary:

```text
Extract the effective graph from V.
That graph is Gamma_eff, the least-squares graph that minimizes nullifier noise.
Draw using Gamma_eff.
Start node coloring with nullifier_var.
Later reuse the same plot function for kurtosis, purity, and other quantities.
```

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
Do not modify files unless the user explicitly says one of:
수정해
파일에 넣어
노트북에 추가해
If the user uses any other wording, ask before editing.
Do not immediately implement the full simulation.
Help design or implement only the next small layer.
```
