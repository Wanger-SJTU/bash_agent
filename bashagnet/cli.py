"""Main CLI entry point using typer."""

from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.syntax import Syntax

from bashagnet.ai.claude import ClaudeProvider
from bashagnet.ai.openai import OpenAIProvider
from bashagnet.config import Config
from bashagnet.core.executor import CommandExecutor

console = Console()


def main(
    prompt: str = typer.Argument(
        None,
        help="Natural language prompt or command to execute",
    ),
    model: str = typer.Option(
        None,
        "--model", "-m",
        help="AI model to use",
    ),
    provider: str = typer.Option(
        None,
        "--provider", "-p",
        help="AI provider (claude, openai, local)",
    ),
    config: Optional[Path] = typer.Option(
        None,
        "--config", "-c",
        help="Path to config file",
    ),
    interactive: bool = typer.Option(
        False,
        "--interactive", "-i",
        help="Start interactive mode",
    ),
    execute: bool = typer.Option(
        False,
        "--execute", "-x",
        help="Execute the generated command",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Show command without executing",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose", "-v",
        help="Verbose output",
    ),
    version: bool = typer.Option(
        False,
        "--version",
        help="Show version and exit",
    ),
):
    """Bashagnet - AI-enhanced bash shell agent."""
    # Show version
    if version:
        from bashagnet import __version__

        console.print(f"bashagnet v{__version__}")
        raise typer.Exit()

    # Load configuration
    if config:
        cfg = Config.load_from_file(config)
    else:
        cfg = Config.load_default()

    # Override config with CLI options
    if model:
        cfg.ai.model = model
    if provider:
        cfg.ai.provider = provider

    # Interactive mode
    if interactive:
        from bashagnet.shell.interactive import run_interactive

        run_interactive(cfg)
        raise typer.Exit()

    # Direct command mode (requires prompt)
    if not prompt:
        console.print("[bold]Bashagnet[/bold] - AI-enhanced bash shell agent\n")
        console.print("Usage:")
        console.print("  bashagnet [OPTIONS] PROMPT")
        console.print("  bashagnet --interactive\n")
        console.print("Options:")
        console.print("  -h, --help     Show this help")
        console.print("  --version      Show version")
        console.print("  -i, --interactive  Interactive mode")
        console.print("  -x, --execute  Execute generated command")
        console.print("\nExamples:")
        console.print("  bashagnet 'list all python files'")
        console.print("  bashagnet -i")
        raise typer.Exit(0)

    # Execute in direct mode
    asyncio_run(prompt, cfg, execute, dry_run, verbose)


def asyncio_run(prompt: str, cfg: Config, execute: bool, dry_run: bool, verbose: bool):
    """Run async command generation."""
    import asyncio

    async def _run():
        # Get AI provider
        ai_provider = get_ai_provider(cfg)

        # Generate command
        console.print(f"\n[bold blue]Generating command for:[/bold blue] {prompt}\n")

        response = await ai_provider.generate(prompt)

        # Show response
        if response.explanation:
            console.print(Panel(response.explanation, title="Explanation", border_style="blue"))

        if response.command:
            console.print(Panel(
                Syntax(response.command, "bash", theme="monokai"),
                title="Generated Command",
                border_style="green" if not response.dangerous else "red",
            ))

        # Safety check
        if response.command and response.dangerous:
            console.print("\n[red bold]⚠️  Warning: This command may be dangerous![/red bold]")
            if not execute:
                console.print("[yellow]Use --execute to run it anyway[/yellow]")
                return

        # Execute if requested
        if response.command and (execute or dry_run):
            if dry_run:
                console.print("\n[yellow][Dry run] Command would be executed[/yellow]")
                return

            executor = CommandExecutor()

            # Safety validation
            safety = ai_provider.validate_command(
                response.command,
                cfg.security.dangerous_commands,
            )

            if not safety.safe:
                console.print(f"\n[red]Safety check failed:[/red] {safety.reason}")
                if cfg.security.require_confirmation:
                    console.print("[yellow]Use --execute to run anyway[/yellow]")
                    return

            # Execute command
            console.print("\n[bold]Executing...[/bold]")
            result = await executor.execute(response.command)

            # Show result
            if result.stdout:
                console.print(result.stdout)

            if result.stderr:
                console.print(f"[red]{result.stderr}[/red]")

            if result.success:
                console.print(f"\n[green]✓ Exit code: {result.exit_code}[/green]")
            else:
                console.print(f"\n[red]✗ Exit code: {result.exit_code}[/red]")

    try:
        asyncio.run(_run())
    except ValueError as e:
        # Show user-friendly error message (API key issues, etc.)
        console.print(f"\n[red]Error:[/red] {e}")
        raise typer.Exit(1)
    except Exception as e:
        # Show generic error for unexpected issues
        if verbose:
            # In verbose mode, show full traceback
            raise
        else:
            # Otherwise show friendly message
            console.print(f"\n[red]An error occurred:[/red] {e}")
            console.print("[yellow]Use --verbose for more details[/yellow]")
            raise typer.Exit(1)


def get_ai_provider(cfg: Config):
    """Get AI provider instance based on config."""
    if cfg.ai.provider == "claude":
        return ClaudeProvider(cfg.ai.dict())
    elif cfg.ai.provider == "openai":
        return OpenAIProvider(cfg.ai.dict())
    else:
        console.print(f"[red]Error: Provider '{cfg.ai.provider}' not supported[/red]")
        console.print("Currently supported: claude, openai")
        raise typer.Exit(1)


def app():
    """Entry point for typer."""
    typer.run(main)


if __name__ == "__main__":
    app()
