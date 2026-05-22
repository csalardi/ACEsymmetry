from pathlib import Path
import subprocess
import typer

def launch():
    "Launcher of the ACEsymmetry application"
    typer.run(main)

def main():
    app_path:Path=Path(__file__).parent/"Interface.py"
    subprocess.run(["streamlit","run",app_path])

if __name__ == "__main__":
    launch()