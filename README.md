# 2026file

## conda 세팅

```bash
conda activate exp
python -m pip install ipykernel
python -m ipykernel install --user --name exp --display-name "Python (exp)"
```

## 패키지 설치

```bash
conda activate exp
python -m pip install package_name
```

설치 후 Jupyter Notebook에서 kernel restart.

## git 처음 세팅

```bash
git init
git add simul.ipynb README.md
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/jihyeoks/2026file.git
git pull origin main --allow-unrelated-histories --no-rebase --no-edit
git push -u origin main
```

## 수정시_명령어

```bash
git status
git add .
git commit -m "Update files"
git push
```

## 확인용_명령어

```bash
git status
git remote -v
```
