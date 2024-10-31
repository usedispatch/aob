import typer
import os
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
from typing import Optional
from pathlib import Path

# data = {
#     "name": "Rick",
#     "age": 42,
#     "items": [{"name": "Portal Gun"}, {"name": "Plumbus"}],
#     "active": True,
#     "affiliation": None,
# }



# def main():
#     print("Here's the data")
#     rprint(data)


# if __name__ == "__main__":
#     typer.run(main)


# Initialize Typer app and Rich console
app = typer.Typer(
    name="aox",
    help="CLI tool for managing and running AO Counter",
    add_completion=False
)
console = Console()

def get_repo_path() -> Path:
    """Get the path to the AO Counter repository"""
    return Path.home() / ".aox" / "ao-counter"


@app.command()
def init(
    force: bool = typer.Option(
        False,
        "--force", "-f",
        help="Force re-initialization even if repository exists"
    )
):
    """Initialize by cloning the AO Counter repository"""
    repo_url = "https://github.com/usedispatch/ao-counter"
    target_dir = get_repo_path()
    print(target_dir)
    with console.status("[bold blue]Initializing AO Counter...") as status:
        if target_dir.exists() and not force:
            console.print(Panel.fit(
                "[yellow]AO Counter repository already exists\n"
                "Use --force to reinitialize",
                title="Warning"
            ))
            return
        
        try:
            # if force and target_dir.exists():
            #     shutil.rmtree(target_dir)
            
            target_dir.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                ["git", "clone", repo_url, str(target_dir)],
                check=True,
                capture_output=True
            )
            
            console.print(Panel.fit(
                "[green]Successfully initialized AO Counter",
                title="Success"
            ))
            
        except subprocess.CalledProcessError as e:
            console.print(Panel.fit(
                f"[red]Failed to clone repository\nError: {e.stderr.decode()}",
                title="Error"
            ))
            raise typer.Exit(1)
        except Exception as e:
            console.print(Panel.fit(
                f"[red]An error occurred: {str(e)}",
                title="Error"
            ))
            raise typer.Exit(1)

if __name__ == "__main__":
    app()

# @app.command()
# def init(
#     force: bool = typer.Option(
#         False,
#         "--force", "-f",
#         help="Force re-initialization even if repository exists"
#     )
# ):
#     """Initialize by cloning the AO Counter repository"""
#     repo_url = "https://github.com/usedispatch/ao-counter"
#     target_dir = get_repo_path()
    
#     with console.status("[bold blue]Initializing AO Counter...") as status:
#         if target_dir.exists() and not force:
#             console.print(Panel.fit(
#                 "[yellow]AO Counter repository already exists\n"
#                 "Use --force to reinitialize",
#                 title="Warning"
#             ))
#             return
        
#         try:
#             if force and target_dir.exists():
#                 import shutil
#                 shutil.rmtree(target_dir)
            
#             target_dir.parent.mkdir(parents=True, exist_ok=True)
#             subprocess.run(
#                 ["git", "clone", repo_url, str(target_dir)],
#                 check=True,
#                 capture_output=True
#             )
            
#             console.print(Panel.fit(
#                 "[green]Successfully initialized AO Counter",
#                 title="Success"
#             ))
            
#         except subprocess.CalledProcessError as e:
#             console.print(Panel.fit(
#                 f"[red]Failed to clone repository\nError: {e.stderr.decode()}",
#                 title="Error"
#             ))
#             raise typer.Exit(1)
#         except Exception as e:
#             console.print(Panel.fit(
#                 f"[red]An error occurred: {str(e)}",
#                 title="Error"
#             ))
#             raise typer.Exit(1)

# @app.command()
# def run(
#     verbose: bool = typer.Option(
#         False,
#         "--verbose", "-v",
#         help="Show detailed output"
#     )
# ):
#     """Run the AO Counter code"""
#     repo_dir = get_repo_path()
    
#     if not repo_dir.exists():
#         console.print(Panel.fit(
#             "[red]AO Counter not initialized\n"
#             "Please run 'aox init' first",
#             title="Error"
#         ))
#         raise typer.Exit(1)
    
#     try:
#         with console.status("[bold blue]Running AO Counter...") as status:
#             # Change to the repository directory
#             os.chdir(repo_dir)
            
#             # Run the main script
#             result = subprocess.run(
#                 ["python", "main.py"],
#                 check=True,
#                 capture_output=not verbose,
#                 text=True
#             )
            
#             if verbose and result.stdout:
#                 console.print(result.stdout)
            
#             console.print(Panel.fit(
#                 "[green]Successfully ran AO Counter",
#                 title="Success"
#             ))
            
#     except subprocess.CalledProcessError as e:
#         console.print(Panel.fit(
#             f"[red]Failed to run AO Counter\nError: {e.stderr}",
#             title="Error"
#         ))
#         raise typer.Exit(1)
#     except Exception as e:
#         console.print(Panel.fit(
#             f"[red]An error occurred: {str(e)}",
#             title="Error"
#         ))
#         raise typer.Exit(1)

# if __name__ == "__main__":
#     app()
