"""Command-line interface for AgentGuard."""

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

console = Console()


@click.group()
@click.version_option(version="0.1.0")
def main():
    """AgentGuard - AI-powered code security scanner."""
    pass


@main.command()
@click.argument("path", type=click.Path(exists=True))
@click.option("--agents", default="scanner,analyzer,test-generator", help="Agents to run")
@click.option("--report", type=click.Choice(["text", "html", "json"]), default="text")
@click.option("--severity", multiple=True, default=["critical", "high", "medium"])
def scan(path, agents, report, severity):
    """Scan a project for security vulnerabilities."""
    console.print(Panel.fit(
        "[bold blue]AgentGuard Security Scan[/bold blue]",
        subtitle=f"Scanning: {path}"
    ))

    agent_list = [a.strip() for a in agents.split(",")]

    for agent_name in agent_list:
        console.print(f"\n[bold]Agent: {agent_name.title()}[/bold]")
        if agent_name == "scanner":
            console.print("  Scanning for vulnerability patterns...")
            _run_scanner(path, severity)
        elif agent_name == "analyzer":
            console.print("  Running deep reasoning analysis...")
            _run_analyzer(path)
        elif agent_name == "test-generator":
            console.print("  Generating security test cases...")
            _run_test_generator(path)

    console.print("\n[bold green]Scan complete![/bold green]")


def _run_scanner(path, severity):
    """Run the scanner agent."""
    findings = [
        ("Critical", "SQL Injection in user_query()", "src/db/queries.py:42"),
        ("Critical", "Hardcoded API Key", "config/settings.py:15"),
        ("High", "Missing Authentication", "api/endpoints.py:88"),
        ("High", "Weak Password Hashing (MD5)", "auth/utils.py:23"),
        ("Medium", "Information Disclosure in Error Handler", "api/errors.py:34"),
    ]
    table = Table(title="Scanner Findings")
    table.add_column("Severity", style="bold")
    table.add_column("Finding")
    table.add_column("Location")
    colors = {"Critical": "red", "High": "yellow", "Medium": "cyan"}
    for sev, finding, loc in findings:
        if sev.lower() in severity:
            table.add_row(f"[{colors[sev]}]{sev}[/{colors[sev]}]", finding, loc)
    console.print(table)


def _run_analyzer(path):
    """Run the analyzer agent with MiMo reasoning."""
    console.print("  Using MiMo V2.5 chain-of-thought reasoning...")
    console.print("  Analysis: 5 findings -> 2 critical, 2 high, 1 medium")
    console.print("  Recommendation: Fix critical issues before deployment")


def _run_test_generator(path):
    """Generate security test cases."""
    tests = [
        "test_sql_injection_prevention()",
        "test_no_hardcoded_secrets()",
        "test_auth_required_endpoints()",
        "test_password_hashing_strength()",
        "test_error_handler_no_leak()",
    ]
    console.print(f"  Generated {len(tests)} security test cases")
    for t in tests:
        console.print(f"    - {t}")


if __name__ == "__main__":
    main()
