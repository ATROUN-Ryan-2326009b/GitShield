from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from github_scanner import scan_github_repo
from risk_score import (
    count_threatening_files,
    count_medium_files,
    get_risk_color
)


console = Console()


def show_banner():
    banner = Text()
    banner.append("GitShield\n", style="bold cyan")
    banner.append("Advanced GitHub Security Scanner\n", style="white")
    banner.append("by Frizz", style="bold green")

    console.print(
        Panel.fit(
            banner,
            border_style="cyan",
            padding=(1, 4)
        )
    )


def build_summary_panel(report):
    score = report["score"]
    color = get_risk_color(score)

    threatening_files = count_threatening_files(report["file_results"])
    medium_files = count_medium_files(report["file_results"])

    content = (
        f"[bold]Repository:[/bold] {report['repo_url']}\n"
        f"[bold]Branch scanned:[/bold] {report['branch']}\n\n"
        f"[bold]Total files analyzed:[/bold] {report['total_files']}\n"
        f"[bold]Skipped files:[/bold] {report['skipped_files']}\n"
        f"[bold]Suspicious files:[/bold] {len(report['file_results'])}\n"
        f"[bold]Medium risk files:[/bold] {medium_files}\n"
        f"[bold]Threatening files:[/bold] {threatening_files}\n\n"
        f"[bold]Security risk score:[/bold] [{color}]{score}%[/{color}]\n"
        f"[bold]Verdict:[/bold] [{color}]{report['verdict']}[/{color}]"
    )

    return Panel(
        content,
        title="GitShield Report",
        border_style=color
    )


def show_top_files(file_results):
    if not file_results:
        console.print("[green]No suspicious file detected.[/green]")
        return

    table = Table(title="Top Risk Files", show_lines=True)

    table.add_column("File", style="cyan", overflow="fold")
    table.add_column("Score", justify="center")
    table.add_column("Categories", style="magenta", overflow="fold")
    table.add_column("Matched patterns", style="white", overflow="fold")

    sorted_results = sorted(
        file_results,
        key=lambda item: item["score"],
        reverse=True
    )

    for result in sorted_results[:8]:
        patterns = sorted(set(finding["pattern"] for finding in result["findings"]))

        table.add_row(
            result["file"],
            f"{result['score']}%",
            ", ".join(result["categories"]),
            ", ".join(patterns[:6])
        )

    console.print(table)


def show_recommendation(score):
    if score >= 75:
        message = (
            "[red]Recommendation:[/red] Do not run this repository directly. "
            "Review the flagged files manually in an isolated environment."
        )
        border = "red"
    elif score >= 45:
        message = (
            "[yellow]Recommendation:[/yellow] Be careful. "
            "Manual review is recommended before running the code."
        )
        border = "yellow"
    elif score >= 15:
        message = (
            "[cyan]Recommendation:[/cyan] Low risk detected. "
            "The repository does not look malicious, but review flagged files if needed."
        )
        border = "cyan"
    else:
        message = (
            "[green]Recommendation:[/green] No obvious threat detected. "
            "This does not guarantee the repository is safe."
        )
        border = "green"

    console.print(Panel(message, border_style=border))


def main():
    show_banner()

    repo_url = console.input("[bold]Enter GitHub repo URL:[/bold] ")

    try:
        with Progress(
            SpinnerColumn(),
            TextColumn("[bold blue]Scanning repository without git clone..."),
            transient=True
        ) as progress:
            progress.add_task("scan", total=None)
            report = scan_github_repo(repo_url)

    except Exception as error:
        console.print(
            Panel(
                f"[red]Scan failed:[/red]\n{error}",
                title="GitShield Error",
                border_style="red"
            )
        )
        return

    console.print()
    console.print(build_summary_panel(report))
    console.print()
    show_top_files(report["file_results"])
    console.print()
    show_recommendation(report["score"])


if __name__ == "__main__":
    main()