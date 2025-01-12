"""
Module to create a new project locally and optionally on GitHub.

This module sets up a new project directory with a specified structure,
initializes a Git repository, and optionally creates a remote repository on GitHub.
"""

import os
import sys

from github import Github, GithubException

# Constants
GITHUB_LOCAL_DIRECTORY = os.environ.get("github-local-directory")
GITHUB_TOKEN = os.environ.get("github-token")
LOG_LEVELS_FILE = "logs/log_levels.info"


def get_command_line_args():
    """
    Fetch folder name and action type from command-line arguments.

    Returns:
        tuple: folder name and action type
    """
    folder_name = str(sys.argv[1])
    action_type = str(sys.argv[2])  # 'g' for GitHub integration, 'l' for local only
    return folder_name, action_type


def setup_github_api(token):
    """
    Set up GitHub API.

    Args:
        token (str): GitHub token

    Returns:
        tuple: GitHub user object and login name
    """
    github_instance = Github(token)
    user = github_instance.get_user()
    return user, user.login


def create_github_repo(user, repo_name):
    """
    Create a new repository on GitHub.

    Args:
        user (github.AuthenticatedUser.AuthenticatedUser): GitHub user object
        repo_name (str): Name of the repository

    Returns:
        str: URL of the created repository
    """
    repo = user.create_repo(repo_name)
    print(f"Repository '{repo}' created on GitHub.")
    return f"https://github.com/{user.login}/{repo_name}.git"


def get_directory_structure():
    """
    Get the directory structure for the new project.

    Returns:
        dict: Directory structure
    """
    return {
        "cmd": "cmd",
        "logs": "logs",
        "config": "config",
        "src": "src",
        "app": "src/app",
        "tests": "src/tests",
        "data": "data",
        "data_input": "data/input",
        "data_output": "data/output",
        "data_archive": "data/archive",
        "docs": "docs",
    }


def get_placeholder_content(repo_name):
    """
    Get placeholder content for various files.

    Args:
        repo_name (str): Name of the repository

    Returns:
        tuple: Placeholder content for pyproject.toml, LICENSE, and main script
    """
    pyproject_toml = f"""
[project]
name = "{repo_name}"
version = "0.1.0"
description = "A Python project"
authors = [{{ name = "Your Name", email = "your.email@example.com" }}]
license = "MIT"
dependencies = []

[build-system]
requires = ["setuptools>=42", "wheel"]
build-backend = "setuptools.build_meta"
"""
    license_content = f"""
MIT License

Copyright (c) {repo_name}

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

[Full MIT license text here...]
"""
    main_script = f"""
import logging
import os

# Logging configuration
script_dir = os.path.dirname(__file__)
logs_path = os.path.join(script_dir, "..", "..", "logs", "{repo_name}.log")

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
    logger.info("Application started.")

if __name__ == "__main__":
    main()
"""
    return pyproject_toml, license_content, main_script


def get_git_commands(repo_name, repo_url):
    """
    Get Git commands to initialize and push to GitHub.

    Args:
        repo_name (str): Name of the repository
        repo_url (str): URL of the remote repository

    Returns:
        list: List of Git commands
    """
    commands = [
        f"echo # {repo_name} > README.md",
        "echo __pycache__/ > .gitignore",
        "echo *.code > .gitignore",
        "echo *.vscode > .gitignore",
        "echo *.idea > .gitignore",
        "echo *local_env > .gitignore",
        "echo *venv > .gitignore",
        "echo *.venv > .gitignore",
        "echo requests > requirements.txt",
        "mkdir cmd",
        f"echo @echo off > cmd/{repo_name}.cmd",
        "mkdir config",
        f"echo KEY=Value > config/{repo_name}.env",
        "mkdir logs",
        "echo INFO > logs/log_levels.info",
        "mkdir src",
        "mkdir src/app",
        "mkdir src/tests",
        "mkdir data",
        "mkdir data/input",
        "mkdir data/output",
        "mkdir data/archive",
        "mkdir docs",
        "git init",
        "git add .",
        'git commit -m "Initial commit"',
    ]

    if repo_url:
        commands += [
            "git branch -M main",
            f"git remote add origin {repo_url}",
            "git push -u origin main",
            "git checkout -b develop",
        ]

    return commands


def create_project_directory_structure(base_path, dirs):
    """
    Create the project directory structure.

    Args:
        base_path (str): Base path for the project
        dirs (dict): Directory structure
    """
    os.mkdir(base_path)
    os.chdir(base_path)

    for directory in dirs.values():
        os.makedirs(directory, exist_ok=True)


def write_placeholder_files(dirs, pyproject_toml, license_content, main_script):
    """
    Write placeholder files in the project directory.

    Args:
        dirs (dict): Directory structure
        pyproject_toml (str): Content for pyproject.toml
        license_content (str): Content for LICENSE
        main_script (str): Content for main script
    """
    with open(f"{dirs['app']}/main.py", "w", encoding="utf-8") as main_file:
        main_file.write(main_script)

    with open(f"{dirs['tests']}/test_main.py", "w", encoding="utf-8") as test_file:
        test_file.write("import pytest\n\ndef test_example():\n    assert True\n")

    with open("LICENSE", "w", encoding="utf-8") as license_file:
        license_file.write(license_content)

    with open("pyproject.toml", "w", encoding="utf-8") as pyproject_file:
        pyproject_file.write(pyproject_toml)

    with open(f"{dirs['app']}/__init__.py", "w", encoding="utf-8") as init_file:
        init_file.write("# Initialization file for the package")


def execute_commands(commands):
    """
    Execute a list of system commands.

    Args:
        commands (list): List of commands to execute
    """
    for command in commands:
        print(f"Executing command: {command}")
        os.system(command)


def main():
    """
    Main function to create a new project locally and optionally on GitHub.
    """
    folder_name, action_type = get_command_line_args()
    base_path = os.path.join(GITHUB_LOCAL_DIRECTORY, folder_name)

    user, _ = setup_github_api(GITHUB_TOKEN)
    repo_url = create_github_repo(user, folder_name) if action_type == "g" else None

    dirs = get_directory_structure()
    pyproject_toml, license_content, main_script = get_placeholder_content(folder_name)
    git_commands = get_git_commands(folder_name, repo_url)

    try:
        create_project_directory_structure(base_path, dirs)
        write_placeholder_files(dirs, pyproject_toml, license_content, main_script)
        execute_commands(git_commands)

        print(f"Project '{folder_name}' created successfully at {base_path}")

        # Open the project in VS Code
        os.system("code .")

    except (OSError, IOError, GithubException) as error:
        print(f"Error: {error}")
        print("Failed to create project.")


if __name__ == "__main__":
    main()
