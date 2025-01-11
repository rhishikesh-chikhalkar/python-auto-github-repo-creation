import os
import sys

foldername = str(sys.argv[1])
path = os.environ.get("github-local-directory")
print(f"path: {path}")
_dir = path + "/" + foldername

try:
    os.mkdir(_dir)
    os.chdir(_dir)
    os.system("git init")
    os.system(f'echo "# {foldername}" > README.md')
    os.system("git add README.md")
    os.system('git commit -m "first commit"')

    print(f"{foldername} created locally")
    os.system("code .")
except Exception:
    print("create <project_name> l")
