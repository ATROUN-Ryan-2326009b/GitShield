import time
import itertools
import threading

from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

from github_scanner import scan_github_repo
from risk_score import count_threatening_files

console = Console()
loading = True


def show_banner():
    console.print(Panel.fit(
        "[bold cyan]GitShield[/bold cyan]\n"
        "[white]Advanced GitHub Security Scanner[/white]\n"
        "[green]by Frizz[/green]",
        border_style="cyan"
    ))


def display_results(score, verdict, file_results, total_files):
    threatening_files = count_threatening_files(file_results)

    # Couleur dynamique
    if score >= 75:
        color = "red"
    elif score >= 45:
        color = "yellow"
    else:
        color = "green"

    console.print("\n")

    console.print(Panel(
        f"[bold]Total files:[/bold] {total_files}\n"
        f"[bold]Suspicious files:[/bold] {len(file_results)}\n"
        f"[bold]Threatening files:[/bold] {threatening_files}\n\n"
        f"[bold]Risk Score:[/bold] [{color}]{score}%[/{color}]\n"
        f"[bold]Verdict:[/bold] [{color}]{verdict}[/{color}]",
        title="GitShield Report",
        border_style=color
    ))

    if file_results:
        table = Table(title="Top Risk Files", show_lines=True)

        table.add_column("File", style="cyan")
        table.add_column("Score", justify="center")
        table.add_column("Categories", style="magenta")

        sorted_results = sorted(
            file_results,
            key=lambda x: x["score"],
            reverse=True
        )

        for result in sorted_results[:5]:
            table.add_row(
                result["file"],
                f"{result['score']}%",
                ", ".join(result["categories"])
            )

        console.print(table)


def main():
    show_banner()

    repo_url = console.input("[bold]Enter GitHub repo URL:[/bold] ")

    with Progress(
        SpinnerColumn(),
        TextColumn("[bold blue]Scanning repository..."),
        transient=True
    ) as progress:
        progress.add_task("scan", total=None)

        score, verdict, file_results, total_files = scan_github_repo(repo_url)

    display_results(score, verdict, file_results, total_files)


if __name__ == "__main__":
    main()