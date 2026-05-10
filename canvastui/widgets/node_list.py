"""
Node list widget for displaying and selecting canvas nodes.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from rich.text import Text
from textual.message import Message
from textual.widgets import Static, ListView, ListItem, Label
from textual.containers import Vertical

from canvastui.canvas_parser import CanvasFile, CanvasNode

if TYPE_CHECKING:
    from textual.app import ComposeResult


class NodeListWidget(Vertical):
    """
    Widget for displaying a list of canvas nodes.
    
    Supports selection, filtering, and search highlighting.
    """
    
    class NodeSelected(Message):
        """Message sent when a node is selected."""
        def __init__(self, node: CanvasNode) -> None:
            super().__init__()
            self.node = node
    
    def __init__(
        self,
        canvas: Optional[CanvasFile] = None,
        *,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, classes=classes)
        self.canvas = canvas or CanvasFile()
        self._filtered_nodes: list[CanvasNode] = []
        self._selected_index = -1
    
    def compose(self) -> ComposeResult:
        """Compose the widget."""
        yield ListView(id="node-list-view")
    
    def on_mount(self) -> None:
        """Handle mount."""
        self._populate_list()
    
    def update_canvas(self, canvas: CanvasFile) -> None:
        """Update the canvas and refresh the list."""
        self.canvas = canvas
        self._populate_list()
    
    def _populate_list(self, nodes: Optional[list[CanvasNode]] = None) -> None:
        """Populate the list with nodes."""
        nodes_to_show = nodes or self.canvas.nodes
        self._filtered_nodes = nodes_to_show
        
        try:
            list_view = self.query_one("#node-list-view", ListView)
            list_view.clear()
            
            for node in nodes_to_show:
                # Create label with node info
                text = self._format_node_label(node)
                label = Label(text, classes=f"node-item node-{node.node_type.value}")
                list_view.append(ListItem(label, id=f"node-{node.node_id[:8]}"))
        except Exception:
            pass
    
    def _format_node_label(self, node: CanvasNode) -> Text:
        """Format a node label for display."""
        text = Text()
        
        # Type icon
        icons = {
            "text": "📝",
            "file": "📄",
            "link": "🔗",
            "group": "📦",
        }
        icon = icons.get(node.node_type.value, "•")
        text.append(f"{icon} ", style="bold")
        
        # Content preview
        content = node.text[:30] if node.text else node.file or node.url or node.label or "Empty"
        if len(content) > 30:
            content = content[:27] + "..."
        text.append(content)
        
        return text
    
    def show_search_results(self, nodes: list[CanvasNode]) -> None:
        """Show search results in the list."""
        self._populate_list(nodes)
    
    def select_next(self) -> None:
        """Select the next node."""
        if not self._filtered_nodes:
            return
        
        self._selected_index = min(
            self._selected_index + 1,
            len(self._filtered_nodes) - 1
        )
        self._update_selection()
    
    def select_previous(self) -> None:
        """Select the previous node."""
        if not self._filtered_nodes:
            return
        
        self._selected_index = max(self._selected_index - 1, 0)
        self._update_selection()
    
    def _update_selection(self) -> None:
        """Update the visual selection."""
        try:
            list_view = self.query_one("#node-list-view", ListView)
            if 0 <= self._selected_index < len(self._filtered_nodes):
                list_view.index = self._selected_index
        except Exception:
            pass
    
    def get_selected_node(self) -> Optional[CanvasNode]:
        """Get the currently selected node."""
        if 0 <= self._selected_index < len(self._filtered_nodes):
            return self._filtered_nodes[self._selected_index]
        return None
    
    def on_list_view_selected(self, event: ListView.Selected) -> None:
        """Handle list selection."""
        try:
            index = event.list_view.index
            if index is not None and 0 <= index < len(self._filtered_nodes):
                self._selected_index = index
                node = self._filtered_nodes[index]
                self.post_message(self.NodeSelected(node))
        except Exception:
            pass
