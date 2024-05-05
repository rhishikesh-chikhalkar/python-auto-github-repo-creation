import os
import sys

from github import Github

foldername = str(sys.argv[1])
path = os.environ.get("mp")  # add projects dirctory to the env vars
token = os.environ.get("gt")  # add github token to the env vars
_dir = path + "/" + foldername

g = Github(token)
user = g.get_user()
login = user.login
repo = user.create_repo(foldername)


cmd_dir = "cmd"
logs_dir = "logs"
config_dir = "config"
src_dir = "src"
repo_name = repo.name.replace("-", "_")
log_file_path = os.path.join(logs_dir, "log_levels.info")

# Read the contents of the info file
with open(log_file_path, "r") as log_file:
    log_info_contents = log_file.read().strip()

code = f"""
import logging
import os

# Get the current directory of the script
script_dir = os.path.dirname(__file__)
logs_path = os.path.join(script_dir, "..", "logs", "{repo_name}.log")

# Logging Configuration
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

file_handler = logging.FileHandler(logs_path, mode="a")
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

stream_handler = logging.StreamHandler()
stream_handler.setFormatter(formatter)

logger.addHandler(file_handler)
logger.addHandler(stream_handler)

def main():
    pass

if __name__ == "__main__":
    main()
"""


commands = [
    f"(echo # {repo.name} ) > README.md",
    "(echo *__pycache__ && echo *.code && echo *.vscode && echo *.idea && echo *local_env && echo *venv && echo *.venv) > .gitignore",
    f"mkdir {cmd_dir}",
    f"(echo @echo off) > {cmd_dir}/{repo_name}.cmd",
    f"mkdir {config_dir}",
    f"(echo KEY=Value) > {config_dir}/{repo_name}.env",
    f"mkdir {logs_dir}",
    "echo '' > logs/log_levels.info",
    f"mkdir {src_dir}",
    f"(echo '') > {src_dir}/main.py",
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
        print(f"command: {c}")
        os.system(c)

    # Write the code to a file named main.py
    with open(f"{src_dir}/main.py", "w") as file:
        file.write(code)

    with open(f"{logs_dir}/log_levels.info", "w") as file:
        file.write(log_info_contents)

    print(f"{foldername} created locally")
    os.system("code .")  # add github token to the env vars

else:
    print("create <fldername>")
