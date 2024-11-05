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

TOOL_VERSION = "0.0.1"

app = typer.Typer(
    name="aox",
    help="CLI tool for Scaffolding,Deploying and Generating AO Apps",
    add_completion=False
)
console = Console()

def get_repo_path() -> Path:
    """Get the path to the AO Counter repository in current directory"""
    return Path.cwd() / "ao-counter"


@app.command(name="version")
def version():
    """Display the current version of AOX CLI"""
    console.print(f"AOX CLI version {TOOL_VERSION}")

@app.command(name="init")
def init(force: bool = typer.Option(False, "--force", "-f", help="Force re-initialization even if repository exists"),
         path: str = typer.Option(None, "--path", "-p", help="Custom installation path (defaults to current directory)")):
    """Initialize a new AO Counter project"""
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
                console.print(Panel.fit("[yellow]Installation already exists at this location\nUse --force to reinstall", title="⚠️ Warning"))
                return
            else:
                with console.status("[yellow]Cleaning existing installation...", spinner="dots"):
                    import shutil
                    shutil.rmtree(target_dir)

        # Create directory structure
        target_dir.parent.mkdir(parents=True, exist_ok=True)
        
        progress_columns = [
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ]
        
        with Progress(*progress_columns, expand=True) as progress:
            # Clone repository
            clone_task = progress.add_task("Cloning repository...", total=100)
            
            # Start git clone process
            process = subprocess.Popen(
                ["git", "clone", repo_url, str(target_dir)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            while process.poll() is None:
                progress.update(clone_task, advance=1)
                time.sleep(0.1)
            
            progress.update(clone_task, completed=100)
            
            if process.returncode != 0:
                error = process.stderr.read().decode().strip()
                raise subprocess.CalledProcessError(process.returncode, "git clone", error)

            # Root yarn install
            root_install_task = progress.add_task("Installing dependencies...", total=100)
            
            os.chdir(target_dir)
            process = subprocess.Popen(
                ["yarn", "install"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            while process.poll() is None:
                progress.update(root_install_task, advance=1)
                time.sleep(0.1)
            
            progress.update(root_install_task, completed=100)
            
            if process.returncode != 0:
                error = process.stderr.read().decode().strip()
                raise subprocess.CalledProcessError(process.returncode, "yarn install", error)

            # App yarn install  
            app_install_task = progress.add_task("Installing app dependencies...", total=100)
            
            os.chdir(target_dir / "app")
            process = subprocess.Popen(
                ["yarn", "install"],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE
            )
            
            while process.poll() is None:
                progress.update(app_install_task, advance=1)
                time.sleep(0.1)
            
            progress.update(app_install_task, completed=100)
            
            if process.returncode != 0:
                error = process.stderr.read().decode().strip()
                raise subprocess.CalledProcessError(process.returncode, "yarn install", error)

        # Show success message
        console.print(Panel.fit(
            "[green bold]✓ AO Counter installed successfully!\n\n"
            "[white]Next steps:[/white]\n"
            f"1. cd into the repository: [cyan]cd {target_dir}[/cyan]\n",
            title="Installation Complete",
            border_style="green"
        ))

    except subprocess.CalledProcessError as e:
        console.print(Panel.fit(f"[red]Failed to clone repository\nError: {e.stderr}", title="❌ Error", border_style="red"))
        raise typer.Exit(1)
    except Exception as e:
        console.print(Panel.fit(f"[red]An error occurred: {str(e)}", title="❌ Error", border_style="red"))
        raise typer.Exit(1)
    

@app.command(name="deploy")
def deploy(
    component: str = typer.Argument(..., help="Component to deploy (process/frontend)")
):
    """Deploy AO Counter components (process or frontend)"""
    if component not in ["process", "frontend"]:
        console.print(Panel.fit(
            "[red]Invalid component. Must be either 'process' or 'frontend'",
            title="❌ Error",
            border_style="red"
        ))
        raise typer.Exit(1)

    # Check if we're in a valid AO Counter project directory
    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        console.print(Panel.fit(
            "[red]No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO Counter project.",
            title="❌ Error",
            border_style="red"
        ))
        raise typer.Exit(1)

    try:
        if component == "process":
            # Process deployment logic
            console.print("\n[bold blue]Deploying AO Counter Process[/bold blue]")
            command = "process:deploy"
            success_message = "Process deployed successfully!"
        else:
            # Frontend deployment logic 
            console.print("\n[bold blue]Deploying AO Counter Frontend[/bold blue]")
            command = "frontend:build"
            success_message = "Frontend built successfully!"
            
        with console.status(f"[bold blue]Running {command}...", spinner="dots"):
            # Run the deployment command
            process = subprocess.run(
                ["yarn", command],
                capture_output=True,
                text=True
            )
            
            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode,
                    f"yarn {command}",
                    process.stderr
                )

        # Show success message
        console.print(Panel.fit(
            f"[green bold]✓ {success_message}",
            title="Deployment Complete",
            border_style="green"
        ))

    except subprocess.CalledProcessError as e:
        console.print(Panel.fit(
            f"[red]Deployment failed\nError: {e.stderr}",
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
    

@app.command(name="build")
def build(
    component: str = typer.Argument(..., help="Component to build (process/frontend)")
):
    """Build AO Counter components (process or frontend)"""
    if component not in ["process", "frontend"]:
        console.print(Panel.fit(
            "[red]Invalid component. Must be either 'process' or 'frontend'",
            title="❌ Error",
            border_style="red"
        ))
        raise typer.Exit(1)

    # Check if we're in a valid AO Counter project directory
    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        console.print(Panel.fit(
            "[red]No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO Counter project.",
            title="❌ Error",
            border_style="red"
        ))
        raise typer.Exit(1)

    try:
        if component == "process":
            # Process deployment logic
            console.print("\n[bold blue]Building AO Counter Process[/bold blue]")
            command = "process:build"
            success_message = "Process built successfully!"
        else:
            # Frontend deployment logic 
            console.print("\n[bold blue]Deploying AO Counter Frontend[/bold blue]")
            command = "frontend:build"
            success_message = "Frontend built successfully!"
            
        with console.status(f"[bold blue]Running {command}...", spinner="dots"):
            # Run the deployment command
            process = subprocess.run(
                ["yarn", command],
                capture_output=True,
                text=True
            )
        
            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode,
                    f"yarn {command}",
                    process.stderr
                )

        # Show success message
        console.print(Panel.fit(
            f"[green bold]✓ {success_message}",
            title="Build Complete",
            border_style="green"
        ))

    except subprocess.CalledProcessError as e:
        console.print(Panel.fit(
            f"[red]Deployment failed\nError: {e.stderr}",
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
