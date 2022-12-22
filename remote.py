import sys
import os
from github import Github

foldername = str(sys.argv[1])
path = os.environ.get("mp")  # add projects dirctory to the env vars
token = os.environ.get("gt")  # add github token to the env vars
_dir = path + "/" + foldername

g = Github(token)
user = g.get_user()
login = user.login
repo = user.create_repo(foldername)

commands = [
    f"(echo # {repo.name} ) >README.md",
    "(echo *__pycache__ && echo *.code && echo *.vscode && echo *.idea && echo *local_env && echo *venv) >.gitignore",
    "git init",
    "git add .",
    'git commit -m "Initial commit"',
    "git branch -M main",
    f"git remote add origin https://github.com/{login}/{foldername}.git",
    "git push -u origin main",
    "git checkout -b develop",
]

if sys.argv[2] == "g":
    os.mkdir(_dir)
    os.chdir(_dir)

    for c in commands:
        os.system(c)

    print(f"{foldername} created locally")
    os.system("code .")  # add github token to the env vars

else:
    print("create <fldername>")
