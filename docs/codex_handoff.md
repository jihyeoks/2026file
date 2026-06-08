# Codex Handoff

## Project

This repository is for a Jupyter notebook simulation of photon-subtracted
continuous-variable graph states, based mainly on:

- Mattia Walschaers et al., "Tailoring Non-Gaussian Continuous-Variable Graph States", Phys. Rev. Lett. 121, 220501 (2018).
- Additional reference: `PhysRevA.96.053835.pdf`.

The goal is to reproduce the simulation logic step by step inside notebooks,
not to rush into a full Python package.

## Current Files

- `simul.ipynb`: main working notebook. Current graph is the 6-node paper-style
  test graph.
- `simul_test.ipynb`: new test notebook. Current graph is a triangular lattice
  made by `triangular_lattice_adjacency(n_rows)`.
- `docs/codex_handoff.md`: this handoff file.
- `README.md`: should stay short and command-focused.

No `main.py` is needed at the current stage.

## Reference PDFs

Local reference paths used on the original machine:

```text
/Users/jujoun/Desktop/!photon subtraction 관련/Reference/교수님의 권유/Phys Rev Lett 2018 Walschaers.pdf
/Users/jujoun/Desktop/!photon subtraction 관련/Reference/교수님의 권유/PhysRevA.96.053835.pdf
```

If working on another computer, copy or relink these papers as needed.

## User Preferences

- Absolute editing gate: do not modify notebook/code files unless the user
  explicitly says one of these exact Korean trigger phrases:
  - `수정해`
  - `파일에 넣어`
  - `노트북에 추가해`
- If the user says exploratory phrases like `만들어볼까`, `해볼까`,
  `생각해보자`, or `코드 짜볼까`, do not treat it as permission to edit.
  Ask for confirmation before modifying files.
- Reading files, explaining, planning, and showing code drafts in chat are OK.
- If the user explicitly asks to update/create the handoff file, modify only
  `docs/codex_handoff.md` unless they name another file.
- Do not jump directly into a full implementation. Help design or implement the
  next small layer.
- Prefer notebook-first development. Move code into Python modules only later,
  after functions become stable.

Important recent mistake:

```text
On 2026-05-21, Codex edited simul.ipynb after discussion without one of the
required trigger phrases. Do not repeat this.
```

## Mathematical Convention

Quadrature ordering:

```text
q = (x_1, ..., x_m, p_1, ..., p_m)^T
```

Vacuum variance convention:

```text
Var(x_vac) = Var(p_vac) = 1
```

Use 0-based indexing internally in Python. Use 1-based labels only for display
if helpful.

Main objects:

```text
Adj    : graph adjacency matrix / CZ topology
G      : CV CZ symplectic matrix, paper notation
V0     : initial Gaussian covariance matrix
V      : graph-state covariance, V = G @ V0 @ G.T
f_sub  : complex subtraction-mode vector in C^m
g_sub  : real phase-space subtraction vector
Jg_sub : J @ g_sub
Pi_g   : g_sub g_sub.T + Jg_sub Jg_sub.T
```

Do not store the quantum state in a NetworkX graph. NetworkX is only for
visualization and graph utilities.

## Current Notebook Flow

Current implemented flow in `simul.ipynb`:

```text
1. Set the graph state
   - imports: numpy, networkx, matplotlib, pandas
   - define Adj, m, Omega, J
   - define CZ symplectic matrix G = [[I, 0], [Adj, I]]
   - define V0 with 10 dB squeezing and vacuum variance 1
   - compute V = G @ V0 @ G.T
   - define f_sub, g_sub, Jg_sub, Pi_g

2. Plotting / visualization helpers
   - custom colormaps: blue, red
   - plot_graph_from_matrix(...)
   - show_mat(...)
   - draw_mat(...)

3. Graph-state sanity / effective nullifier graph
   - split V into V_xx, V_xp, V_px, V_pp
   - compute Gamma1 for p - Gamma x
   - compute Gamma2 for x - Gamma p
   - choose smaller trace residual
   - set Gamma_eff, V_delta, nullifier_var
   - plot effective nullifier graph

4. Photon Subtraction on the graph
   - compute A_minus
   - compute node-wise p-quadrature excess kurtosis K_ex_p
   - color graph nodes by K_ex_p
```

`simul_test.ipynb` mirrors this flow for a triangular lattice test. It defines:

```text
triangular_lattice_adjacency(n_rows)
```

For the current test:

```text
n_rows = 12
total nodes = n_rows * (n_rows + 1) / 2 = 78
f_sub is a single center-ish lattice node
sub_label = f"center mode {center_idx + 1}"
```

## Graph Construction

For the 6-node paper-style graph in `simul.ipynb`, `Adj` is explicitly written
as a 6 by 6 matrix.

For the triangular lattice in `simul_test.ipynb`, `triangular_lattice_adjacency`
returns:

```text
Adj : symmetric adjacency matrix
pos : triangular drawing positions using 0-based NetworkX node indices
idx : map from lattice coordinate (r, c) to node index
```

The triangular layout uses:

```text
x = c - r / 2
y = -sqrt(3) / 2 * r
```

When using `nx.from_numpy_array`, node indices are `0, 1, ..., m-1`. Display
labels may still be shown as `1, 2, ..., m`.

## Effective Nullifier Graph

Given:

```text
V = [[V_xx, V_xp],
     [V_px, V_pp]]
```

compute two least-squares nullifier directions:

```text
delta_1 = p - Gamma1 x
Gamma1 = V_px @ pinv(V_xx)

delta_2 = x - Gamma2 p
Gamma2 = V_xp @ pinv(V_pp)
```

Residual covariances:

```text
Vd1 = V_pp - Gamma1 @ V_xp - V_px @ Gamma1.T + Gamma1 @ V_xx @ Gamma1.T
Vd2 = V_xx - Gamma2 @ V_px - V_xp @ Gamma2.T + Gamma2 @ V_pp @ Gamma2.T
```

Choose the smaller trace:

```text
if trace(Vd1) <= trace(Vd2):
    Gamma_eff = Gamma1
    V_delta = Vd1
    nullifier_type = "p - Gamma x"
else:
    Gamma_eff = Gamma2
    V_delta = Vd2
    nullifier_type = "x - Gamma p"
```

Then:

```text
nullifier_var = diag(V_delta)
```

For the ideal graph state generated by:

```text
G = [[I, 0], [Adj, I]]
V = G @ V0 @ G.T
```

the first direction should win and `Gamma1` should approximately equal `Adj`.

## Plotting Helpers

### `plot_graph_from_matrix`

Current signature:

```python
plot_graph_from_matrix(
    W,
    node_values=None,
    title="",
    threshold=1e-6,
    pos=None,
    cmap=blue,
    vmin=None,
    vmax=None,
    colorbar_label="",
    draw_labels=None
)
```

Current behavior:

- Converts `W` to `W_plot = np.array(W, dtype=float).copy()`.
- Creates `G_plot = nx.from_numpy_array(W_plot)`.
- If `pos is None`, uses `nx.kamada_kawai_layout(G_plot)`.
- Labels are displayed as `i + 1`.
- If `node_values is None`, node labels are shown by default.
- If `node_values` exists, labels are hidden by default unless
  `draw_labels=True`.
- Uses `plt.axis("equal")` and `plt.axis("off")`.
- Returns `pos` so later plots can reuse the same layout.

For larger graphs in `simul_test.ipynb`, the function adapts figure size,
node size, font size, and edge width based on the number of nodes.

Note: Earlier plans discussed symmetrizing `Gamma_eff` for plotting. Current
notebook code does not do that inside `plot_graph_from_matrix`. If this matters,
discuss before changing the notebook.

### Matrix Display

Current matrix helpers:

```python
show_mat(M, name="M", digits=3, tol=1e-10)
draw_mat(M, title="", cmap="bwr", label=False, digits=2, vlim=None, figsize=(4.5, 4))
```

`show_mat`:

- Zeroes tiny values under `tol`.
- Uses `pandas.DataFrame(...).style.format(...)`.
- Gives a readable numeric matrix table with 1-based row/column labels.

`draw_mat`:

- Uses `imshow` with a diverging colormap.
- Shows row/column ticks as 1-based indices.
- Uses `vlim` if given, otherwise the 95th percentile of absolute values.
- If `label=True`, writes numbers inside the cells.

User preference from discussion:

```text
For matrices, the user wants the numbers to be visible and the result to look
like a matrix, not just a heatmap. Keep helper functions short and practical.
```

## Photon Subtraction Layer

The current implemented layer computes:

```text
V, Pi_g -> A_minus -> node-wise p-quadrature excess kurtosis K_ex_p
```

Do not build the full density matrix or Wigner function yet.

### A Matrix

Formula:

```text
A_minus = 2 * (V - I) Pi_g (V - I) / Tr[(V - I) Pi_g]
```

Current code structure:

```python
I_2m = np.eye(2 * m)
denom = np.trace((V - I_2m) @ Pi_g)

if np.isclose(denom, 0):
    raise ValueError("denom is close to zero: photon subtraction mode may be vacuum-like.")

A_minus = 2 * (V - I_2m) @ Pi_g @ (V - I_2m) / denom
```

Current sanity prints:

```python
print("Pi_g projector check:", bool(np.linalg.norm(Pi_g @ Pi_g - Pi_g)) < 1e-10)
print("A_minus symmetric check:", bool(np.linalg.norm(A_minus - A_minus.T) < 1e-10))
```

Note: `denom` is currently described in comments as related to photon
subtraction success probability. If precision matters, verify this convention
against the paper before using it quantitatively.

### Node-wise p-quadrature Excess Kurtosis

With ordering:

```text
q = (x_1, ..., x_m, p_1, ..., p_m)^T
```

the p indices are:

```python
p_indices = np.arange(m, 2 * m)
```

Current formula:

```python
v_p = np.diag(V)[p_indices]
a_p = np.diag(A_minus)[p_indices]
K_ex_p = -3 * (a_p ** 2) / ((v_p + a_p) ** 2)
```

Interpretation:

```text
v_p    : p-quadrature variances before photon subtraction
a_p    : p-quadrature diagonal contribution from A_minus
K_ex_p : node-wise p-quadrature excess kurtosis
```

Graph coloring:

```python
pos = plot_graph_from_matrix(
    Gamma_eff,
    node_values=K_ex_p,
    title=f"p-quad Excess Kurtosis \nsubtracted at {sub_label}",
    pos=pos,
    draw_labels=False  # simul.ipynb
)
```

In `simul_test.ipynb`, the current call uses `draw_labels=True`.

## Planned Homodyne Measurement Layer

This section is a planned next coding layer for the part after:

```text
## 3. Homodyne Measurement
```

Do not implement it unless the user explicitly asks to modify the notebook.
The user wants to compare two orders of operations:

```text
3.1 photon subtraction first, then homodyne deletion/feedforward
3.2 homodyne deletion/feedforward first, then photon subtraction
```

Recommended title for the matrix layer:

```text
Gaussian envelope and non-Gaussian matrix layer
```

Shorter acceptable title:

```text
V,A matrix layer
```

Important convention:

```text
V       : Gaussian envelope covariance in Mattia/Walschaers notation
V + A   : actual covariance after photon subtraction
```

Deletion/feedforward gain must be computed from the photon-subtraction-before
Gaussian envelope `V`, not from `V + A`.

### Shared Homodyne Deletion Setup

Let:

```text
H : measured/deleted node set
R : remaining node set = {1, ..., N} \ H
j : photon-subtracted target node
```

Required condition:

```text
j not in H
```

For derivation, reorder the full quadrature vector as:

```text
q_full = (q_R, x_H, p_H)^T
```

where `q_R` contains both x and p quadratures of the remaining nodes.

The Gaussian deletion/feedforward gain is:

```text
K = V_{q_R x_H} @ inv(V_{x_H x_H})
```

The feedforward linear map is:

```text
q_R_ff = q_R - K x_H
L = [I, -K, 0]
```

The common Gaussian envelope after deletion/feedforward is:

```text
V_R_ff = L @ V @ L.T
```

Equivalently:

```text
V_R_ff = V_{q_R q_R} - V_{q_R x_H} @ inv(V_{x_H x_H}) @ V_{x_H q_R}
```

### Case 3.1: Photon Subtraction First

Initial variables:

```text
V
A_j = A_j(V)
H
j, with j not in H
```

Here `A_j(V)` is the full-space non-Gaussian matrix generated by photon
subtraction at node `j` before deletion.

Compute the same Gaussian feedforward map `L` from `V`, then transform both
the Gaussian envelope and the non-Gaussian correction:

```text
V_R_ff = L @ V @ L.T
A_3_1 = L @ A_j(V) @ L.T
```

Block expression for the A matrix:

```text
A_3_1
= A_{q_R q_R}
  - K @ A_{x_H q_R}
  - A_{q_R x_H} @ K.T
  + K @ A_{x_H x_H} @ K.T
```

The final characteristic function is:

```text
chi_3_1(alpha_R)
= exp[-1/2 alpha_R.T @ V_R_ff @ alpha_R]
  * [1 - 1/2 alpha_R.T @ A_3_1 @ alpha_R]
```

The actual covariance for this case is:

```text
V_actual_3_1 = V_R_ff + A_3_1
```

### Case 3.2: Photon Subtraction Later

Initial variables:

```text
V
H
j, with j not in H
```

First perform the Gaussian homodyne deletion/feedforward:

```text
V_R_ff = L @ V @ L.T
```

Then compute photon subtraction on the reduced graph:

```text
A_3_2 = A_j(V_R_ff)
```

For photon subtraction:

```text
A_3_2
= 2 * (V_R_ff - I_R) @ Pi_j_R @ (V_R_ff - I_R)
  / Tr[(V_R_ff - I_R) @ Pi_j_R]
```

Important:

```text
Pi_j_R is the projector for node j in the reduced R-space,
not the original full-space projector.
```

The final characteristic function is:

```text
chi_3_2(alpha_R)
= exp[-1/2 alpha_R.T @ V_R_ff @ alpha_R]
  * [1 - 1/2 alpha_R.T @ A_3_2 @ alpha_R]
```

The actual covariance for this case is:

```text
V_actual_3_2 = V_R_ff + A_3_2
```

### Graph-Layer Analysis After Homodyne

Both cases should reuse the same graph-layer analysis functions. Only the
input `A` matrix changes:

```text
Case 3.1: V_env = V_R_ff, A = A_3_1
Case 3.2: V_env = V_R_ff, A = A_3_2
```

For a target node `j in R`, construct reduced-space unit vectors:

```text
f = e_{x_j}^{(R)}
f = e_{p_j}^{(R)}
```

Then compute:

```text
v_f = f.T @ V_R_ff @ f
a_f = f.T @ A @ f
K_ex(f) = -3 * a_f**2 / (v_f + a_f)**2
```

Use the same later observables already discussed:

```text
min W_j
negativity volume
single-node Wigner function W_j(x, p)
```

### Core Comparison

Both orders produce the same Gaussian envelope:

```text
V_env_3_1 = V_env_3_2 = V_R_ff = L @ V @ L.T
```

The only intended difference is the non-Gaussian A matrix:

```text
Case 3.1: A_3_1 = L @ A_j(V) @ L.T
Case 3.2: A_3_2 = A_j(L @ V @ L.T)
```

Therefore the central comparison is:

```text
L @ A_j(V) @ L.T
vs
A_j(L @ V @ L.T)
```

## Sanity Checks

Dimension/shape checks remain useful:

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

Further physics checks can come later:

```text
V is symmetric
V is physical
G is symplectic
nullifier variance is correct
```

For 10 dB p-squeezed input with vacuum variance 1, expected ideal nullifier
variance is:

```text
0.1
```

## Next Likely Tasks

Good next steps:

```text
1. Verify the A_minus / K_ex_p formulas against the reference paper notation.
2. Decide whether A_minus should be explicitly symmetrized numerically.
3. Decide whether Gamma_eff plotting should use raw Gamma_eff or a plotting-only symmetrized matrix.
4. Clean up duplicated helper functions between simul.ipynb and simul_test.ipynb only when the notebook workflow stabilizes.
5. Test smaller graphs first when debugging, then return to the triangular lattice.
```

Later observables:

```text
purity ratio mu / mu_Gauss
single-mode Wigner function W_k(q,p)
other node-wise quantities
```

## Test Graph Order

Recommended debugging order:

```text
1. 3-node line graph
2. 6-node paper-style graph
3. 7-node line graph
4. small triangular lattice
5. larger triangular lattice / Fig. 3-like graph
```

Do not debug first on the large triangular lattice if something basic breaks.

## Recommended Interaction Style

When continuing this project with Codex:

```text
First read docs/codex_handoff.md.
Then inspect simul.ipynb and, if relevant, simul_test.ipynb.
Do not modify notebooks unless the user explicitly says one of:
수정해
파일에 넣어
노트북에 추가해
If the user asks to update this handoff, edit only docs/codex_handoff.md.
Do not immediately implement the full simulation.
Help design or implement only the next small layer.
```
