
from pathlib import Path

# Main project folder
project_name = "Automated-Resume-Screening-Tool"

# Folder structure
folders = [
    "resumes",
    "data",
    "src",
    "outputs",
    "images",
    "docs"
]

# Files to create
files = [
    "main.py",
    "requirements.txt",
    "README.md",
    ".gitignore"
]

# Create main folder
project_path = Path(project_name)
project_path.mkdir(exist_ok=True)

# Create subfolders
for folder in folders:
    (project_path / folder).mkdir(exist_ok=True)

# Create files
for file in files:
    (project_path / file).touch(exist_ok=True)

print("Project structure created successfully!")

print("\nYour project contains:")
for item in sorted(project_path.iterdir()):
    print(item.name)
