import os
import ast
import subprocess

# Set the path to the project folder
path = os.path.dirname(os.path.realpath(__file__))

# Get a list of all Python files in the project folder
python_files = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.py') and not f.startswith('__init__')]

# Get a list of the current file's dependencies
current_file = os.path.basename(__file__)
with open(current_file, 'r') as f:
    tree = ast.parse(f.read())
    current_dependencies = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for name in node.names:
                current_dependencies.add(name.name)
        elif isinstance(node, ast.ImportFrom):
            current_dependencies.add(node.module)

# Loop through each Python file and extract the dependencies
dependencies = set()
for python_file in python_files:
    if os.path.basename(python_file) == current_file:
        continue
    with open(python_file, 'r') as f:
        tree = ast.parse(f.read())
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for name in node.names:
                    dependencies.add(name.name)
            elif isinstance(node, ast.ImportFrom):
                dependencies.add(node.module)

# Install the dependencies using pip
installed_dependencies = []
failed_dependencies = []
for dependency in dependencies:
    if dependency in current_dependencies:
        continue
    result = subprocess.run(['pip', 'install', dependency], capture_output=True)
    if result.returncode == 0:
        installed_dependencies.append(dependency)
    else:
        failed_dependencies.append(dependency)

# Print the results
print(f"Successfully installed {len(installed_dependencies)} dependencies:")
print(installed_dependencies)
print(f"Failed to install {len(failed_dependencies)} dependencies:")
print(failed_dependencies)
