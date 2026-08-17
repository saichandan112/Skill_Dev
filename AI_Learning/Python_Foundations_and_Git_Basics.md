# Python Foundations & Git — Essentials

A concise reference covering the basics you need to start Python development and Git version control.

---

## Python Foundations

### Installation & Environment
- Install Python 3.10+ from python.org or use Anaconda/Miniconda.
- Create a project virtual environment:

```bash
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS / Linux
source .venv/bin/activate
```

- Upgrade pip and install common packages:

```bash
pip install --upgrade pip
pip install numpy pandas matplotlib scikit-learn jupyterlab
```

- Use `requirements.txt` to pin dependencies:

```bash
pip freeze > requirements.txt
pip install -r requirements.txt
```

### Basic Syntax & Types
- Numbers: `int`, `float`
- Text: `str`
- Bool: `bool`
- Containers: `list`, `tuple`, `set`, `dict`

Example:
```python
x = 10
name = "Alice"
nums = [1, 2, 3]
pair = (1, 'a')
lookup = {'a': 1, 'b': 2}
```

### Control Flow
- If/elif/else
- For & while loops
- Comprehensions

Example:
```python
if x > 0:
    print('positive')

for i in range(5):
    print(i)

squares = [i*i for i in range(10)]
```

### Functions & Modules
- Define with `def`, return values, default args, *args/**kwargs
- Organize code into modules and packages (use `__init__.py`)

Example:
```python
def greet(name: str = 'World') -> str:
    return f"Hello, {name}!"
```

### File I/O
```python
with open('data.txt', 'r', encoding='utf-8') as f:
    text = f.read()

with open('out.txt', 'w', encoding='utf-8') as f:
    f.write('hello')
```

### Error Handling
```python
try:
    result = 10 / x
except ZeroDivisionError:
    result = None
finally:
    cleanup()
```

### Object-Oriented Basics
```python
class Employee:
    def __init__(self, name, id):
        self.name = name
        self.id = id

    def __repr__(self):
        return f"Employee({self.name!r}, {self.id})"
```

### Useful Standard Library Modules
- `os`, `pathlib` (filesystem)
- `json`, `csv` (data interchange)
- `datetime` (dates/times)
- `logging` (app logs)
- `unittest` / `pytest` (testing)

### Testing & Linting
- Write tests with `pytest`:

```bash
pip install pytest
pytest
```

- Use `flake8` or `pylint` for style checks, and `black` for formatting.

### Running Scripts & Notebooks
- Python script: `python script.py`
- Jupyter Lab / Notebook: `jupyter lab`

---

## Git Basics

### Setup
```bash
git config --global user.name "Your Name"
git config --global user.email "you@example.com"
```

### Initialize / Clone
```bash
git init                # initialize repository
git clone <repo_url>    # clone remote repo
```

### Common Workflow
```bash
git status              # check working tree
git add file.py         # stage changes
git commit -m "msg"    # commit staged changes
git push origin main    # push to remote
git pull origin main    # fetch & merge
```

### Branching & Merging
```bash
git checkout -b feature/x   # create & switch
git checkout main           # switch back
git merge feature/x         # merge into current branch
```

### Rebasing (advanced)
```bash
git checkout feature
git rebase main
# resolve conflicts if any, then:
git rebase --continue
```

### Remote Management
```bash
git remote -v
git remote add origin <url>
git push -u origin feature/x
```

### Undoing Changes
- Unstage: `git restore --staged file.py` (or `git reset HEAD file.py`)
- Discard work: `git restore file.py`
- Amend last commit: `git commit --amend`
- Revert a commit (create new commit that undoes): `git revert <sha>`

### .gitignore
- Add files/folders to ignore (venv, __pycache__, .ipynb_checkpoints)
Example `.gitignore` lines:
```
.venv/
__pycache__/
*.pyc
.DS_Store
.ipynb_checkpoints/
```

### Collaboration (GitHub)
- Fork vs branch strategy
- Create a Pull Request (PR) for code review
- Use descriptive commit messages and small PRs
- Protect main branch with CI checks

### Useful Commands Cheat Sheet
- `git log --oneline --graph --all`
- `git diff` (unstaged changes)
- `git show <commit>`
- `git stash` / `git stash pop`

---

## Quick Project Setup Checklist
1. Create repo and clone it.
2. Create `.venv` and activate it.
3. Add `requirements.txt` and `README.md`.
4. Add `.gitignore`.
5. Make an initial commit and push.

Commands:
```bash
git init
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin <url>
git push -u origin main
```

---

## Learning Exercises (starter)
- Python:
  - Write functions to parse CSV and compute aggregates.
  - Implement classes for a small domain model (Todo app, Employee manager).
  - Practice list/dict comprehensions and generators.
- Git:
  - Create a feature branch, make multiple commits, open a PR on GitHub.
  - Practice resolving a merge conflict locally.

---

_End of essentials. Add this file to your `AI_Learning` folder and iterate as you learn._