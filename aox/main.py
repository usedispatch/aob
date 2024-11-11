"""CLI tool for managing and deploying AO Counter applications."""

import os
import pty
import shutil
import subprocess
import time
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.progress import (
    BarColumn,
    Progress,
    SpinnerColumn,
    TextColumn,
    TimeRemainingColumn,
)

TOOL_VERSION = "0.0.1"
VERBOSE_MODE = False


def log_verbose(message: str):
    """Log a message if verbose mode is enabled."""
    if VERBOSE_MODE:
        console.print(f"[dim]{message}[/dim]")


app = typer.Typer(
    name="aox",
    help="CLI tool for Scaffolding,Deploying and Generating AO Apps.",
    add_completion=False,
)
console = Console()


@app.callback()
def main(
    verbose: bool = typer.Option(False, "--verbose", "-v", help="Enable verbose output")
):
    """Handle the main entry point for the CLI."""
    global VERBOSE_MODE
    VERBOSE_MODE = verbose


def get_repo_path() -> Path:
    """Get the path to the AO Counter repository in current directory."""
    return Path.cwd() / "ao-counter"


@app.command(name="version")
def version():
    """Display the current version of AOX CLI."""
    console.print(f"AOX CLI version {TOOL_VERSION}")


@app.command(name="init")
def init(
    path: str = typer.Option(
        None,
        "--path",
        "-p",
        help="Custom installation path (defaults to current directory)",
    ),
):
    """Initialize a new AO Counter project."""
    repo_url = "https://github.com/usedispatch/ao-counter"
    if path:
        try:
            # Create directory if it doesn't exist
            os.makedirs(path, exist_ok=True)
            # Change to that directory
            os.chdir(path)
            target_dir = Path.cwd()
        except OSError as e:
            show_error_panel("Failed to create or access target directory", str(e))
    else:
        target_dir = Path.cwd()
    log_verbose(f"Target directory: {target_dir}")
    # Show installation header with path info
    console.print("\n[bold blue]AO Counter Installation[/bold blue]")
    console.print("└─ [dim]Repository:[/dim] [cyan]{}[/cyan]".format(repo_url))
    console.print(
        "└─ [dim]Installing to:[/dim] [green]{}[/green]\n".format(target_dir.absolute())
    )
    try:
        # Check existing installation
        if target_dir.exists() and any(target_dir.iterdir()):
            with console.status(
                "[yellow]Cleaning existing installation...", spinner="dots"
            ):
                shutil.rmtree(target_dir)

        # Create directory structure
        target_dir.mkdir(parents=True, exist_ok=True)

        progress_columns = [
            SpinnerColumn(),
            TextColumn("[bold blue]{task.description}"),
            BarColumn(bar_width=40),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
            TimeRemainingColumn(),
        ]

        with Progress(*progress_columns, expand=True) as progress:
            # Clone repository into a temporary directory
            clone_task = progress.add_task("Cloning repository...", total=100)
            temp_dir = target_dir / "temp_ao_counter"
            process = subprocess.Popen(
                ["git", "clone", repo_url, str(temp_dir)],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            while process.poll() is None:
                progress.update(clone_task, advance=1)
                time.sleep(0.1)

            progress.update(clone_task, completed=100)

            if process.returncode != 0:
                error = process.stderr.read().decode().strip()
                raise subprocess.CalledProcessError(
                    process.returncode, "git clone", error
                )

            # Move contents from temp directory to target directory
            for item in temp_dir.iterdir():
                shutil.move(str(item), str(target_dir))

            # Remove the temporary directory
            shutil.rmtree(temp_dir)

            # Root yarn install
            root_install_task = progress.add_task(
                "Installing dependencies...", total=100
            )

            os.chdir(target_dir)
            process = subprocess.Popen(
                ["yarn", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            while process.poll() is None:
                progress.update(root_install_task, advance=1)
                time.sleep(0.1)

            progress.update(root_install_task, completed=100)

            if process.returncode != 0:
                error = process.stderr.read().decode().strip()
                raise subprocess.CalledProcessError(
                    process.returncode, "yarn install", error
                )

            # App yarn install
            app_install_task = progress.add_task(
                "Installing app dependencies...", total=100
            )

            os.chdir(target_dir / "app")
            process = subprocess.Popen(
                ["yarn", "install"], stdout=subprocess.PIPE, stderr=subprocess.PIPE
            )

            while process.poll() is None:
                progress.update(app_install_task, advance=1)
                time.sleep(0.1)

            progress.update(app_install_task, completed=100)

            if process.returncode != 0:
                error = process.stderr.read().decode().strip()
                raise subprocess.CalledProcessError(
                    process.returncode, "yarn install", error
                )

        # Show success message
        show_success_panel(
            "[green bold]✓ AO Counter installed successfully!\n\n"
            "[white]Next steps:[/white]\n"
            "1. Run [cyan]aox dev[/cyan] to start the frontend dev server\n"
            "2. Run [cyan]aox deploy process[/cyan] to deploy the process\n"
            "3. Run [cyan]aox test process[/cyan] to run the process tests",
            "Installation Complete",
        )

    except subprocess.CalledProcessError as e:
        show_error_panel("Failed to clone repository", e.stderr)
    except Exception as e:
        show_error_panel("An error occurred", str(e))


@app.command(name="deploy")
def deploy(
    component: str = typer.Argument(..., help="Component to deploy (process/frontend)")
):
    """Deploy AO Counter components (process or frontend)."""
    if component not in ["process", "frontend"]:
        show_error_panel("Invalid component. Must be either 'process' or 'frontend'")

    # Check if we're in a valid AO Counter project directory
    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        show_error_panel(
            "No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO Counter project."
        )
    try:
        if component == "process":
            console.print("\n[bold blue]Deploying AO Counter Process[/bold blue]")
            command = "deploy:process"
            success_message = "Process deployed successfully!"
        else:
            console.print("\n[bold blue]Deploying AO Counter Frontend[/bold blue]")
            command = "build:frontend"
            success_message = "Frontend built successfully!"

        # Create a pseudo-terminal
        process, master = run_command_with_pty(f"yarn {command}")

        try:
            while True:
                try:
                    # Read from master fd and display output in real-time
                    data = os.read(master, 1024).decode()
                    if data:
                        print(data, end="", flush=True)
                except OSError:
                    break

        finally:
            # Cleanup
            os.close(master)
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, f"yarn {command}"
                )

        # Show success message if we get here
        show_success_panel(success_message, "Deployment Complete")

    except subprocess.CalledProcessError:
        show_error_panel("Deployment failed")
    except Exception as e:
        show_error_panel(f"An error occurred: {str(e)}")


@app.command(name="test")
def test(component: str = typer.Argument(..., help="Component to test (process)")):
    """Run tests for AO Counter components (process)."""
    if component != "process":
        show_error_panel(
            "Invalid component. Currently only 'process' testing is supported"
        )

    # Check if we're in a valid AO Counter project directory
    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        show_error_panel(
            "No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO Counter project."
        )

    try:
        console.print("\n[bold blue]Running AO Counter Process Tests[/bold blue]")
        test_dir = Path.cwd() / "test"
        node_modules = test_dir / "node_modules"

        if not node_modules.exists():
            console.print("\n[yellow]Installing test dependencies...[/yellow]")
            os.chdir(test_dir)

            # Run yarn install in test directory
            process = subprocess.run(
                ["yarn", "install"], capture_output=True, text=True
            )

            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, "yarn install", process.stderr
                )

            # Change back to project root
            os.chdir(test_dir.parent)
            console.print("[green]✓ Test dependencies installed[/green]\n")

        # Create a pseudo-terminal
        process, master = run_command_with_pty("yarn test:process")

        try:
            while True:
                try:
                    # Read from master fd and display output in real-time
                    data = os.read(master, 1024).decode()
                    if not data:  # Process has completed
                        break
                    print(data, end="", flush=True)
                except OSError:  # Read error means process likely completed
                    break

        finally:
            # Cleanup
            os.close(master)
            if process.poll() is None:
                process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

            if process.returncode and process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, "yarn process:test"
                )

        # Show success message if we get here
        show_success_panel("Process tests completed successfully!", "Tests Complete")

    except subprocess.CalledProcessError:
        show_error_panel("Tests failed")
    except Exception as e:
        show_error_panel(f"An error occurred: {str(e)}")


@app.command(name="dev")
def dev():
    """Start the AO Counter frontend development server."""
    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        show_error_panel(
            "No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO Counter project."
        )

    try:
        console.print(
            "\n[bold blue]Starting AO Counter Frontend Development Server[/bold blue]"
        )

        # Create a pseudo-terminal
        process, master = run_command_with_pty("yarn dev:frontend")

        try:
            while True:
                try:
                    # Read from master fd
                    data = os.read(master, 1024).decode()
                    if data:
                        # Print directly to preserve formatting
                        print(data, end="", flush=True)
                except OSError:
                    break

        except KeyboardInterrupt:
            show_error_panel("Development server stopped by user")

        finally:
            # Cleanup
            os.close(master)
            process.terminate()
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                log_verbose("Development server timed out")
                process.kill()

    except Exception as e:
        show_error_panel(f"An error occurred: {str(e)}")


@app.command(name="build")
def build(
    component: str = typer.Argument(..., help="Component to build (process/frontend)")
):
    """Build AO Counter components (process or frontend)."""
    if component not in ["process", "frontend"]:
        console.print(
            Panel.fit(
                "[red]Invalid component. Must be either 'process' or 'frontend'",
                title="❌ Error",
                border_style="red",
            )
        )
        raise typer.Exit(1)

    # Check if we're in a valid AO Counter project directory
    package_json = Path.cwd() / "package.json"
    if not package_json.exists():
        show_error_panel(
            "No package.json found in current directory.\n"
            "Make sure you're in the root directory of an AO Counter project."
        )

    try:
        if component == "process":
            # Process deployment logic
            console.print("\n[bold blue]Building AO Counter Process[/bold blue]")
            command = "build:process"
            success_message = "Process built successfully!"
        else:
            # Frontend deployment logic
            console.print("\n[bold blue]Deploying AO Counter Frontend[/bold blue]")
            command = "build:frontend"
            success_message = "Frontend built successfully!"

        with console.status(f"[bold blue]Running {command}...", spinner="dots"):
            # Run the deployment command
            process = subprocess.run(["yarn", command], capture_output=True, text=True)

            if process.returncode != 0:
                raise subprocess.CalledProcessError(
                    process.returncode, f"yarn {command}", process.stderr
                )
        # Show success message
        show_success_panel(success_message, "Build Complete")

    except subprocess.CalledProcessError as e:
        show_error_panel("Build failed", e.stderr)
    except Exception as e:
        show_error_panel(f"An error occurred: {str(e)}")


def show_success_panel(message: str, title: str = "Complete"):
    """Display a success panel with consistent formatting."""
    console.print(
        Panel.fit(
            f"[green bold]✓ {message}",
            title=title,
            border_style="green",
        )
    )


def show_error_panel(message: str, error_details: str = None):
    """Display an error panel with consistent formatting."""
    log_verbose(f"Error occurred: {error_details or message}")
    error_text = f"[red]{message}"
    if error_details:
        error_text += f"\nError: {error_details}"

    console.print(
        Panel.fit(
            error_text,
            title="❌ Error",
            border_style="red",
        )
    )
    raise typer.Exit(1)


def run_command_with_pty(command: str) -> subprocess.Popen:
    """Run a command with pseudo-terminal support."""
    master, slave = pty.openpty()
    process = subprocess.Popen(
        command,
        shell=True,
        stdin=slave,
        stdout=slave,
        stderr=slave,
        text=True,
        preexec_fn=os.setsid,
        env={**os.environ, "FORCE_COLOR": "1"},
    )
    os.close(slave)
    return process, master


if __name__ == "__main__":
    app()
