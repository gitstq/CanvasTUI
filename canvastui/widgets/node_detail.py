"""
Node detail widget for showing detailed node information.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from rich.console import RenderableType
from rich.text import Text
from rich.panel import Panel
from rich.table import Table
from textual.widgets import Static
from textual.containers import Vertical, ScrollableContainer

from canvastui.canvas_parser import CanvasNode, CanvasFile

if TYPE_CHECKING:
    from textual.app import ComposeResult


class NodeDetailWidget(ScrollableContainer):
    """
    Widget for displaying detailed information about a selected node.
    """
    
    def __init__(
        self,
        node: Optional[CanvasNode] = None,
        *,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, classes=classes)
        self.node = node
    
    def compose(self) -> ComposeResult:
        """Compose the widget."""
        yield Static(id="detail-content", expand=True)
    
    def on_mount(self) -> None:
        """Handle mount."""
        self._update_display()
    
    def update_node(self, node: Optional[CanvasNode]) -> None:
        """Update the displayed node."""
        self.node = node
        self._update_display()
    
    def _update_display(self) -> None:
        """Update the detail display."""
        try:
            content_widget = self.query_one("#detail-content", Static)
            content_widget.update(self._get_detail_renderable())
        except Exception:
            pass
    
    def _get_detail_renderable(self) -> RenderableType:
        """Get the renderable detail content."""
        if not self.node:
            return Text("No node selected", style="dim italic")
        
        node = self.node
        
        # Create info table
        table = Table(show_header=False, box=None, padding=(0, 1))
        table.add_column("Key", style="cyan")
        table.add_column("Value")
        
        # Basic info
        table.add_row("ID", node.node_id)
        table.add_row("Type", node.node_type.value)
        table.add_row("Position", f"({node.x}, {node.y})")
        table.add_row("Size", f"{node.width} × {node.height}")
        
        if node.color:
            table.add_row("Color", node.color)
        
        # Content
        content_lines: list[str] = []
        
        if node.text:
            content_lines.append("📝 Text Content:")
            content_lines.append("")
            # Wrap text for display
            text_lines = node.text.split("\n")
            for line in text_lines[:20]:  # Limit to 20 lines
                content_lines.append(f"  {line}")
            if len(text_lines) > 20:
                content_lines.append(f"  ... ({len(text_lines) - 20} more lines)")
        
        if node.file:
            content_lines.append(f"📄 File: {node.file}")
        
        if node.url:
            content_lines.append(f"🔗 URL: {node.url}")
        
        if node.label:
            content_lines.append(f"🏷️ Label: {node.label}")
        
        # Combine
        result = Text()
        result.append("Node Details\n", style="bold")
        result.append("─" * 30 + "\n\n")
        
        # Table as string
        from rich.console import Console
        console = Console()
        with console.capture() as capture:
            console.print(table)
        result.append(capture.get())
        
        if content_lines:
            result.append("\n")
            for line in content_lines:
                result.append(f"{line}\n")
        
        return result
