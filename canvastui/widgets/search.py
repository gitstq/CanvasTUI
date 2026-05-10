"""
Search widget for searching nodes in the canvas.
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from textual.message import Message
from textual.widgets import Input, Static
from textual.containers import Horizontal, Vertical

if TYPE_CHECKING:
    from textual.app import ComposeResult


class SearchWidget(Vertical):
    """
    Widget for searching nodes in the canvas.
    
    Provides a search input and displays results.
    """
    
    class Search(Message):
        """Message sent when a search is performed."""
        def __init__(self, query: str) -> None:
            super().__init__()
            self.query = query
    
    def __init__(
        self,
        *,
        id: Optional[str] = None,
        classes: Optional[str] = None,
    ) -> None:
        super().__init__(id=id, classes=classes)
        self._visible = False
    
    def compose(self) -> ComposeResult:
        """Compose the widget."""
        with Horizontal(id="search-container"):
            yield Static("🔍", id="search-icon")
            yield Input(placeholder="Search nodes...", id="search-input")
    
    def on_mount(self) -> None:
        """Handle mount."""
        self.styles.display = "none"
    
    def toggle(self) -> None:
        """Toggle the search widget visibility."""
        self._visible = not self._visible
        
        if self._visible:
            self.styles.display = "block"
            try:
                search_input = self.query_one("#search-input", Input)
                search_input.focus()
            except Exception:
                pass
        else:
            self.styles.display = "none"
            try:
                search_input = self.query_one("#search-input", Input)
                search_input.value = ""
            except Exception:
                pass
    
    def show(self) -> None:
        """Show the search widget."""
        if not self._visible:
            self.toggle()
    
    def hide(self) -> None:
        """Hide the search widget."""
        if self._visible:
            self.toggle()
    
    def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle search input submission."""
        if event.input.id == "search-input":
            query = event.value.strip()
            if query:
                self.post_message(self.Search(query))
    
    def on_key(self, event) -> None:
        """Handle key events."""
        if event.key == "escape":
            self.hide()
