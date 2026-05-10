"""
Canvas view widget for visualizing the canvas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from rich.console import RenderableType
from rich.text import Text
from rich.style import Style
from textual.widgets import Static
from textual.containers import Vertical

from canvastui.canvas_parser import CanvasFile, CanvasNode, CanvasEdge

if TYPE_CHECKING:
    from textual.app import ComposeResult


class CanvasViewWidget(Vertical):
    """
    Widget for visualizing the canvas layout.
    
    Provides a bird's-eye view of nodes and their connections.
    """
    
    def __init__(
        self,
        canvas: Optional[CanvasFile] = None,
        *,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, classes=classes)
        self.canvas = canvas or CanvasFile()
        self._viewport_x = 0
        self._viewport_y = 0
        self._zoom = 1.0
        self._selected_node_id: Optional[str] = None
    
    def compose(self) -> ComposeResult:
        """Compose the widget."""
        yield Static(id="canvas-render", expand=True)
    
    def on_mount(self) -> None:
        """Handle mount."""
        self._render_canvas()
    
    def update_canvas(self, canvas: CanvasFile) -> None:
        """Update the canvas and re-render."""
        self.canvas = canvas
        self._render_canvas()
    
    def select_node(self, node_id: Optional[str]) -> None:
        """Select a node by ID."""
        self._selected_node_id = node_id
        self._render_canvas()
    
    def _render_canvas(self) -> None:
        """Render the canvas view."""
        try:
            render_widget = self.query_one("#canvas-render", Static)
            render_widget.update(self._get_canvas_renderable())
        except Exception:
            pass
    
    def _get_canvas_renderable(self) -> RenderableType:
        """Get the renderable representation of the canvas."""
        if not self.canvas.nodes:
            return Text("No nodes in canvas", style="dim italic")
        
        # Calculate bounds
        bounds = self.canvas.bounds
        min_x, min_y, max_x, max_y = bounds
        
        # Normalize coordinates
        width = max_x - min_x or 1
        height = max_y - min_y or 1
        
        # Create a simple text representation
        lines: list[Text] = []
        
        # Header
        header = Text()
        header.append("Canvas Overview", style="bold cyan")
        header.append(f" ({self.canvas.node_count} nodes, {self.canvas.edge_count} edges)")
        lines.append(header)
        lines.append(Text())
        
        # Node list with positions
        for node in self.canvas.nodes:
            line = Text()
            
            # Selection indicator
            if node.node_id == self._selected_node_id:
                line.append("▶ ", style="bold green")
            else:
                line.append("  ")
            
            # Node type icon
            icons = {
                "text": "📝",
                "file": "📄",
                "link": "🔗",
                "group": "📦",
            }
            icon = icons.get(node.node_type.value, "•")
            line.append(f"{icon} ")
            
            # Position
            line.append(f"[{node.x}, {node.y}] ", style="dim")
            
            # Content preview
            content = node.text[:40] if node.text else node.file or node.url or "Empty"
            if len(content) > 40:
                content = content[:37] + "..."
            line.append(content)
            
            # Color indicator
            if node.color:
                line.append(f" {node.color}", style="dim")
            
            lines.append(line)
        
        # Edges section
        if self.canvas.edges:
            lines.append(Text())
            lines.append(Text("Connections:", style="bold yellow"))
            
            for edge in self.canvas.edges[:10]:  # Limit to 10 edges
                line = Text()
                line.append(f"  {edge.from_node[:8]}")
                line.append(" → ", style="cyan")
                line.append(f"{edge.to_node[:8]}")
                if edge.label:
                    line.append(f" [{edge.label}]", style="dim")
                lines.append(line)
            
            if len(self.canvas.edges) > 10:
                lines.append(Text(f"  ... and {len(self.canvas.edges) - 10} more", style="dim"))
        
        # Combine lines
        result = Text()
        for i, line in enumerate(lines):
            if i > 0:
                result.append("\n")
            result.append(line)
        
        return result
    
    def move_viewport(self, dx: int, dy: int) -> None:
        """Move the viewport."""
        self._viewport_x += dx
        self._viewport_y += dy
        self._render_canvas()
    
    def zoom_in(self) -> None:
        """Zoom in."""
        self._zoom = min(self._zoom * 1.2, 5.0)
        self._render_canvas()
    
    def zoom_out(self) -> None:
        """Zoom out."""
        self._zoom = max(self._zoom / 1.2, 0.2)
        self._render_canvas()
