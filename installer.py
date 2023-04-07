import os
import subprocess

def install_requirements():
    """Install packages from a requirements.txt file using pip"""
    file_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    subprocess.check_call(["pip", "install", "-r", file_path])

# Example usage:
install_requirements()
