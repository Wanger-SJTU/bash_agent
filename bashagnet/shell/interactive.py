"""Interactive shell mode using prompt_toolkit."""

from typing import Optional

from prompt_toolkit import PromptSession
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.lexers import PygmentsLexer
from prompt_toolkit.styles import Style
from pygments.lexers import BashLexer
from rich.console import Console

from bashagnet.ai.claude import ClaudeProvider
from bashagnet.ai.openai import OpenAIProvider
from bashagnet.config import Config
from bashagnet.core.executor import CommandExecutor

console = Console()


def get_ai_provider(cfg: Config):
    """Get AI provider instance based on config."""
    if cfg.ai.provider == "claude":
        return ClaudeProvider(cfg.ai.dict())
    elif cfg.ai.provider == "openai":
        return OpenAIProvider(cfg.ai.dict())
    else:
        console.print(f"[red]Error: Provider '{cfg.ai.provider}' not supported[/red]")
        console.print("Currently supported: claude, openai")
        raise ValueError(f"Unsupported provider: {cfg.ai.provider}")


def run_interactive(cfg: Config):
    """Run interactive REPL."""
    try:
        # Setup prompt
        history = FileHistory(".bashagnet_history")
        session = PromptSession(history=history)

        # Setup styling
        style = Style.from_dict(
            {
                "prompt": "ansigreen bold",
                "command": "ansicyan",
            }
        )

        # Initialize components
        ai_provider = get_ai_provider(cfg)
        executor = CommandExecutor()

        console.print("\n[bold green]Bashagnet Interactive Mode[/bold green]")
        console.print("Type 'help' for commands, 'exit' or Ctrl-D to quit\n")

        while True:
            try:
                # Get user input
                user_input = session.prompt(
                    "bashagnet> ",
                    style=style,
                    lexer=PygmentsLexer(BashLexer),
                    auto_suggest=AutoSuggestFromHistory(),
                )

            if not user_input.strip():
                continue

            # Handle special commands
            if user_input.lower() in ["exit", "quit"]:
                console.print("Goodbye!")
                break

            if user_input.lower() == "help":
                show_help()
                continue

            if user_input.lower() == "clear":
                console.clear()
                continue

            # Process input
            import asyncio

            asyncio.run(process_input(user_input, ai_provider, executor, cfg))

        except KeyboardInterrupt:
            console.print("\n[yellow]Use 'exit' to quit[/yellow]")
        except EOFError:
            console.print("\nGoodbye!")
            break


async def process_input(prompt: str, ai_provider, executor, cfg: Config):
    """Process user input in interactive mode."""
    try:
        console.print(f"\n[bold blue]Processing:[/bold blue] {prompt}\n")

        # Generate command
        response = await ai_provider.generate(prompt)

    # Show explanation
    if response.explanation:
        console.print(f"[dim]{response.explanation}[/dim]\n")

    # Show command
    if response.command:
        console.print(f"[bold cyan]Command:[/bold cyan] {response.command}")

        # Ask for confirmation
        if response.dangerous or not cfg.security.require_confirmation:
            console.print("[red bold]⚠️  Potentially dangerous![/red bold]")

        # Safety check
        safety = ai_provider.validate_command(
            response.command,
            cfg.security.dangerous_commands,
        )

        if not safety.safe:
            console.print(f"[red]Safety warning:[/red] {safety.reason}")

        # Ask for execution
        try:
            confirm = console.input("\n[yellow]Execute? [Y/n]: [/yellow]")
            if confirm.lower() in ["", "y", "yes"]:
                result = await executor.execute(response.command)

                # Show output
                if result.stdout:
                    console.print(result.stdout)

                if result.stderr:
                    console.print(f"[red]{result.stderr}[/red]")

                if result.success:
                    console.print(f"[green]✓ Exit: {result.exit_code}[/green]")
                else:
                    console.print(f"[red]✗ Exit: {result.exit_code}[/red]")
            else:
                console.print("[yellow]Cancelled[/yellow]")
        except KeyboardInterrupt:
            console.print("\n[yellow]Cancelled[/yellow]")
    except ValueError as e:
        # Show user-friendly error for configuration/API issues
        console.print(f"\n[red]Error:[/red] {e}")
    except Exception as e:
        # Show generic error
        console.print(f"\n[red]An error occurred:[/red] {e}")
        console.print("[yellow]Try again or use 'exit' to quit[/yellow]")


def show_help():
    """Show help message."""
    console.print("""
[bold]Bashagnet Interactive Commands:[/bold]

  help    - Show this help message
  clear   - Clear the screen
  exit    - Exit interactive mode

[bold]Usage:[/bold]
  Type natural language commands and bashagnet will:
  1. Generate appropriate bash commands
  2. Show you what will be executed
  3. Ask for confirmation before running

[bold]Examples:[/bold]
  "List all Python files in current directory"
  "Find files larger than 100MB"
  "Show system disk usage"
""")
