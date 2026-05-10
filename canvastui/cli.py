"""
Command-line interface for CanvasTUI.
"""

from __future__ import annotations

import sys
from pathlib import Path
from typing import Optional

import click
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from canvastui import __version__
from canvastui.app import CanvasTUI
from canvastui.canvas_parser import CanvasParser, CanvasFile


console = Console()


def print_banner() -> None:
    """Print the application banner."""
    banner = Text()
    banner.append("🎨 CanvasTUI", style="bold cyan")
    banner.append(" v" + __version__, style="dim")
    banner.append("\n")
    banner.append("Terminal-based JSON Canvas Viewer & Editor", style="italic")
    
    console.print(Panel(banner, border_style="cyan", padding=(1, 2)))


@click.group(invoke_without_command=True)
@click.option("--version", "-v", is_flag=True, help="Show version and exit")
@click.pass_context
def main(ctx: click.Context, version: bool) -> None:
    """
    CanvasTUI - A powerful terminal-based JSON Canvas viewer and editor.
    
    View, navigate, and edit Obsidian Canvas (.canvas) files in your terminal.
    """
    if version:
        console.print(f"CanvasTUI version {__version__}")
        return
    
    if ctx.invoked_subcommand is None:
        # No subcommand provided, show help
        print_banner()
        console.print("\n[bold]Usage:[/bold] canvastui [OPTIONS] COMMAND [ARGS]...\n")
        console.print("[bold]Commands:[/bold]")
        console.print("  open     Open a canvas file in interactive mode")
        console.print("  info     Show information about a canvas file")
        console.print("  list     List all nodes in a canvas file")
        console.print("  search   Search nodes in a canvas file")
        console.print("  new      Create a new empty canvas file")
        console.print("  export   Export canvas to different formats")
        console.print("\n[bold]Examples:[/bold]")
        console.print("  canvastui open my-canvas.canvas")
        console.print("  canvastui info my-canvas.canvas")
        console.print("  canvastui search my-canvas.canvas \"search term\"")


@main.command()
@click.argument("file_path", type=click.Path(exists=True), required=False)
@click.option("--watch", "-w", is_flag=True, help="Watch for file changes")
def open(file_path: Optional[str], watch: bool) -> None:
    """
    Open a canvas file in interactive TUI mode.
    
    If no file is provided, opens an empty canvas.
    """
    print_banner()
    
    canvas_file: Optional[CanvasFile] = None
    
    if file_path:
        try:
            canvas_file = CanvasParser.load(file_path)
            console.print(f"[green]✓[/green] Loaded: {file_path}")
            console.print(f"  Nodes: {canvas_file.node_count}, Edges: {canvas_file.edge_count}")
        except FileNotFoundError:
            console.print(f"[red]✗[/red] File not found: {file_path}")
            sys.exit(1)
        except Exception as e:
            console.print(f"[red]✗[/red] Error loading file: {e}")
            sys.exit(1)
    else:
        canvas_file = CanvasParser.create_empty()
        console.print("[yellow]Opening empty canvas[/yellow]")
    
    # Launch TUI
    app = CanvasTUI(canvas_file=canvas_file, file_path=file_path, watch=watch)
    app.run()


@main.command()
@click.argument("file_path", type=click.Path(exists=True))
def info(file_path: str) -> None:
    """
    Show information about a canvas file.
    """
    try:
        canvas = CanvasParser.load(file_path)
    except Exception as e:
        console.print(f"[red]✗[/red] Error loading file: {e}")
        sys.exit(1)
    
    print_banner()
    
    # File info
    console.print(f"\n[bold]File:[/bold] {file_path}")
    
    # Statistics
    bounds = canvas.bounds
    
    stats_table = Table(show_header=False, box=None)
    stats_table.add_column("Key", style="cyan")
    stats_table.add_column("Value")
    
    stats_table.add_row("Nodes", str(canvas.node_count))
    stats_table.add_row("Edges", str(canvas.edge_count))
    stats_table.add_row("Bounds", f"({bounds[0]}, {bounds[1]}) to ({bounds[2]}, {bounds[3]})")
    
    # Node type breakdown
    node_types: dict[str, int] = {}
    for node in canvas.nodes:
        node_types[node.node_type.value] = node_types.get(node.node_type.value, 0) + 1
    
    if node_types:
        type_str = ", ".join(f"{t}: {c}" for t, c in node_types.items())
        stats_table.add_row("Node Types", type_str)
    
    console.print(stats_table)


@main.command("list")
@click.argument("file_path", type=click.Path(exists=True))
@click.option("--type", "-t", "node_type", help="Filter by node type (text, file, link, group)")
def list_nodes(file_path: str, node_type: Optional[str]) -> None:
    """
    List all nodes in a canvas file.
    """
    try:
        canvas = CanvasParser.load(file_path)
    except Exception as e:
        console.print(f"[red]✗[/red] Error loading file: {e}")
        sys.exit(1)
    
    print_banner()
    
    table = Table(title=f"Nodes in {Path(file_path).name}")
    table.add_column("ID", style="dim", width=10)
    table.add_column("Type", style="cyan", width=8)
    table.add_column("Position", width=15)
    table.add_column("Content", width=50)
    
    for node in canvas.nodes:
        if node_type and node.node_type.value != node_type:
            continue
        
        content = node.text[:47] + "..." if len(node.text) > 50 else node.text
        if not content:
            content = node.file or node.url or node.label or "[dim]empty[/dim]"
        
        table.add_row(
            node.node_id[:8],
            node.node_type.value,
            f"({node.x}, {node.y})",
            content
        )
    
    console.print(table)


@main.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("query")
def search(file_path: str, query: str) -> None:
    """
    Search nodes in a canvas file.
    """
    try:
        canvas = CanvasParser.load(file_path)
    except Exception as e:
        console.print(f"[red]✗[/red] Error loading file: {e}")
        sys.exit(1)
    
    results = canvas.search_nodes(query)
    
    print_banner()
    console.print(f"\n[bold]Search results for:[/bold] '{query}'")
    console.print(f"[dim]Found {len(results)} node(s)[/dim]\n")
    
    for node in results:
        console.print(f"[cyan]•[/cyan] [{node.node_type.value}] {node.node_id[:8]}")
        if node.text:
            # Highlight the search term
            text = node.text[:100] + ("..." if len(node.text) > 100 else "")
            console.print(f"  {text}")
        console.print()


@main.command()
@click.argument("file_path", type=click.Path())
def new(file_path: str) -> None:
    """
    Create a new empty canvas file.
    """
    path = Path(file_path)
    
    if path.exists():
        console.print(f"[red]✗[/red] File already exists: {file_path}")
        sys.exit(1)
    
    canvas = CanvasParser.create_empty()
    CanvasParser.save(canvas, path)
    
    console.print(f"[green]✓[/green] Created new canvas: {file_path}")


@main.command()
@click.argument("file_path", type=click.Path(exists=True))
@click.argument("output", type=click.Path())
@click.option("--format", "-f", "output_format", 
              type=click.Choice(["json", "markdown", "mermaid"]),
              default="json", help="Output format")
def export(file_path: str, output: str, output_format: str) -> None:
    """
    Export canvas to different formats.
    
    Supported formats: json, markdown, mermaid
    """
    try:
        canvas = CanvasParser.load(file_path)
    except Exception as e:
        console.print(f"[red]✗[/red] Error loading file: {e}")
        sys.exit(1)
    
    output_path = Path(output)
    
    if output_format == "json":
        data = CanvasParser.to_dict(canvas)
        import json
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    elif output_format == "markdown":
        content = _export_markdown(canvas)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    elif output_format == "mermaid":
        content = _export_mermaid(canvas)
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(content)
    
    console.print(f"[green]✓[/green] Exported to: {output}")


def _export_markdown(canvas: CanvasFile) -> str:
    """Export canvas to Markdown format."""
    lines = ["# Canvas Export\n"]
    
    for node in canvas.nodes:
        if node.node_type.value == "text":
            lines.append(f"## {node.node_id[:8]}\n")
            lines.append(f"{node.text}\n")
            lines.append(f"*Position: ({node.x}, {node.y})*\n")
    
    return "\n".join(lines)


def _export_mermaid(canvas: CanvasFile) -> str:
    """Export canvas to Mermaid flowchart format."""
    lines = ["graph LR"]
    
    for node in canvas.nodes:
        label = node.text[:20].replace('"', "'") if node.text else node.node_type.value
        lines.append(f'    {node.node_id[:8]}["{label}"]')
    
    for edge in canvas.edges:
        label = f'|{edge.label}|' if edge.label else ''
        lines.append(f'    {edge.from_node[:8]} -->{label} {edge.to_node[:8]}')
    
    return "\n".join(lines)


if __name__ == "__main__":
    main()
