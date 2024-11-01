import typer
import os
import subprocess
import sys
from rich.console import Console
from rich.panel import Panel
from rich import print as rprint
from typing import Optional
from pathlib import Path
import time
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn, TimeRemainingColumn

app = typer.Typer(
    name="aox",
    help="CLI tool for managing and running AO Counter",
    add_completion=False
)
console = Console()

def get_repo_path() -> Path:
    """Get the path to the AO Counter repository in current directory"""
    return Path.cwd() / "ao-counter"


@app.command()
def init(
    force: bool = typer.Option(
        False,
        "--force", "-f",
        help="Force re-initialization even if repository exists"
    ),
    path: str = typer.Option(
        None,
        "--path", "-p", 
        help="Custom installation path (defaults to current directory)"
    )
):
    """Initialize by cloning the AO Counter repository"""
    repo_url = "https://github.com/usedispatch/ao-counter"
    if path:
        target_dir = Path(path) / "ao-counter"
    else:
        target_dir = get_repo_path()

    # Show installation header with path info
    console.print("\n[bold blue]AO Counter Installation[/bold blue]")
    console.print("└─ [dim]Repository:[/dim] [cyan]{}[/cyan]".format(repo_url))
    console.print("└─ [dim]Installing to:[/dim] [green]{}[/green]\n".format(target_dir.absolute()))

    try:
        # Check existing installation
        if target_dir.exists():
            if not force:
                console.print(Panel.fit(
                    "[yellow]Installation already exists at this location\n"
                    "Use --force to reinstall",
                    title="⚠️ Warning"
                ))
                return
            else:
                with console.status("[yellow]Cleaning existing installation...", spinner="dots"):
                    import shutil
                    shutil.rmtree(target_dir)

        # Create directory structure
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        
       
       
        
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
            expand=True
        ) as progress:
            task = progress.add_task("Cloning repository...", total=100)
            
            # Start git clone process
            process = subprocess.Popen(
                ["git", "clone", repo_url, str(target_dir)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            # Update progress while clone is running
            while process.poll() is None:
                progress.update(task, advance=1)
                time.sleep(0.1)
            
            # Ensure we show 100% at the end
            progress.update(task, completed=100)
            
            if process.returncode != 0:
                error = process.stderr.read().decode().strip()
                raise subprocess.CalledProcessError(process.returncode, "git clone", error)

        # Show success message
        console.print(Panel.fit(
            "[green bold]✓ AO Counter installed successfully!\n\n"
            "[white]Next steps:[/white]\n"
            f"1. cd into the repository: [cyan]cd {target_dir}[/cyan]\n",
            title="Installation Complete",
            border_style="green"
        ))

    except subprocess.CalledProcessError as e:
        console.print(Panel.fit(
            f"[red]Failed to clone repository\nError: {e.stderr}",
            title="❌ Error",
            border_style="red"
        ))
        raise typer.Exit(1)
    except Exception as e:
        console.print(Panel.fit(
            f"[red]An error occurred: {str(e)}",
            title="❌ Error",
            border_style="red"
        ))
        raise typer.Exit(1)

if __name__ == "__main__":
    app()
