# 2026file

Photon subtraction simulation notebook repository.

## Files

- `simul.ipynb`: Main Jupyter Notebook for simulation work.

## Python / Conda Environment

This project can be run with a conda environment such as `exp`.

Check available conda environments:

```bash
conda env list
```

Activate the environment:

```bash
conda activate exp
```

Install a package into the active environment:

```bash
python -m pip install package_name
```

After installing a new package from the terminal, restart the Jupyter Notebook kernel in VS Code.

To confirm the notebook is using the correct Python environment, run this in a notebook cell:

```python
import sys
print(sys.executable)
```

Expected example:

```text
/opt/homebrew/anaconda3/envs/exp/bin/python
```

## Jupyter Kernel Setup

If the conda environment does not appear as a Jupyter kernel, register it:

```bash
conda activate exp
python -m pip install ipykernel
python -m ipykernel install --user --name exp --display-name "Python (exp)"
```

Then select `Python (exp)` as the notebook kernel in VS Code.

## Git / GitHub Setup

Initialize git in this folder:

```bash
git init
```

Add the notebook:

```bash
git add simul.ipynb
```

Commit the file:

```bash
git commit -m "Add simulation notebook"
```

Rename the branch to `main`:

```bash
git branch -M main
```

Connect the local repository to GitHub:

```bash
git remote add origin https://github.com/jihyeoks/2026file.git
```

If the GitHub repository already has files such as `README.md`, pull them first:

```bash
git pull origin main --allow-unrelated-histories --no-rebase --no-edit
```

Push local commits to GitHub:

```bash
git push -u origin main
```

## Regular Update Workflow

After editing `simul.ipynb`, use:

```bash
git status
git add simul.ipynb
git commit -m "Update simulation notebook"
git push
```

If `README.md` was also changed:

```bash
git add README.md
git commit -m "Update README"
git push
```

Or add all changed files:

```bash
git add .
git commit -m "Update project files"
git push
```

## Common Git Notes

Check the current git state:

```bash
git status
```

Check the connected GitHub repository:

```bash
git remote -v
```

If `origin` already exists but points to the wrong repository:

```bash
git remote set-url origin https://github.com/jihyeoks/2026file.git
```

If this error appears:

```text
fatal: No configured push destination.
```

Set the upstream branch:

```bash
git push -u origin main
```

If this error appears:

```text
fatal: 'origin' does not appear to be a git repository
```

Add the GitHub remote first:

```bash
git remote add origin https://github.com/jihyeoks/2026file.git
```

Typo note:

```bash
git branch -M main
```

not:

```bash
git brach -M main
```
