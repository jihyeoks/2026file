# 2026file

## Conda 환경 생성

```bash
conda create -n exp python=3.11
conda activate exp
```

## docs에 있는 모듈 설치

### 1) `docs/environment.yml`이 있는 경우

```bash
conda env update -n exp -f docs/environment.yml
```

### 2) `docs/requirements.txt`가 있는 경우

```bash
conda activate exp
pip install -r docs/requirements.txt
```

### 3) 필요한 패키지를 직접 설치하는 경우

```bash
conda activate exp
conda install numpy matplotlib networkx
```

## Jupyter 커널 등록

```bash
python -m pip install ipykernel
python -m ipykernel install --user --name exp --display-name "Python (exp)"
```

설치 후 Jupyter Notebook에서 kernel을 `Python (exp)`로 선택하고 restart하세요.

## git 처음 세팅

### 1) Git 사용자 정보 설정

```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### 2) 로컬 저장소 초기화 및 원격 연결

```bash
git init
git add simul.ipynb README.md
 git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/jihyeoks/2026file.git
git pull origin main --allow-unrelated-histories --no-rebase --no-edit
git push -u origin main
```

> `git config --global`은 이 컴퓨터 전체에 설정됩니다. 한 프로젝트에만 적용하려면 `--global`을 빼고 실행하세요.

## 수정 시 명령어

```bash
git status
git add .
git commit -m "Update files"
git push
```

## 확인용 명령어

```bash
git status
git remote -v
```
