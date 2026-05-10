"""
Main TUI application for CanvasTUI.
"""

from __future__ import annotations

from pathlib import Path
from typing import Optional

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Container, Horizontal, Vertical
from textual.reactive import reactive
from textual.widgets import (
    Footer,
    Header,
    Label,
    Static,
)

from canvastui.canvas_parser import CanvasFile, CanvasNode, CanvasEdge, CanvasParser
from canvastui.widgets.node_list import NodeListWidget
from canvastui.widgets.canvas_view import CanvasViewWidget
from canvastui.widgets.node_detail import NodeDetailWidget
from canvastui.widgets.search import SearchWidget


class CanvasTUI(App):
    """
    Main TUI application for viewing and editing JSON Canvas files.
    
    Features:
    - Interactive canvas navigation
    - Node list with filtering
    - Node detail view
    - Search functionality
    - Real-time file watching
    """
    
    CSS_PATH = "styles.tcss"
    
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("s", "search", "Search", show=True),
        Binding("n", "new_node", "New Node", show=True),
        Binding("e", "edit", "Edit", show=True),
        Binding("d", "delete", "Delete", show=True),
        Binding("w", "toggle_watch", "Watch", show=True),
        Binding("?", "help", "Help", show=True),
        Binding("tab", "focus_next", "Next Panel", show=False),
        Binding("shift+tab", "focus_previous", "Prev Panel", show=False),
        Binding("j", "next_node", "Next Node", show=False),
        Binding("k", "prev_node", "Prev Node", show=False),
        Binding("enter", "select_node", "Select", show=False),
        Binding("escape", "clear_selection", "Clear", show=False),
    ]
    
    # Reactive properties
    current_node: reactive[Optional[CanvasNode]] = reactive(None)
    search_query: reactive[str] = reactive("")
    is_watching: reactive[bool] = reactive(False)
    
    def __init__(
        self,
        canvas_file: Optional[CanvasFile] = None,
        file_path: Optional[str] = None,
        watch: bool = False,
        **kwargs
    ) -> None:
        super().__init__(**kwargs)
        self.canvas = canvas_file or CanvasParser.create_empty()
        self.file_path = Path(file_path) if file_path else None
        self.is_watching = watch
        self._watcher = None
    
    def compose(self) -> ComposeResult:
        """Compose the application layout."""
        yield Header()
        
        with Container(id="main-container"):
            with Horizontal(id="content-area"):
                with Vertical(id="left-panel"):
                    yield Label("📋 Nodes", id="nodes-header")
                    yield NodeListWidget(self.canvas, id="node-list")
                
                with Vertical(id="center-panel"):
                    yield Label("🎨 Canvas", id="canvas-header")
                    yield CanvasViewWidget(self.canvas, id="canvas-view")
                
                with Vertical(id="right-panel"):
                    yield Label("📄 Details", id="detail-header")
                    yield NodeDetailWidget(id="node-detail")
        
        yield SearchWidget(id="search-widget")
        yield Footer()
    
    def on_mount(self) -> None:
        """Handle application mount."""
        self.title = "CanvasTUI"
        self.sub_title = str(self.file_path) if self.file_path else "Untitled"
        
        # Update node list
        self._update_node_list()
        
        # Start file watcher if enabled
        if self.is_watching and self.file_path:
            self._start_watcher()
    
    def on_unmount(self) -> None:
        """Handle application unmount."""
        if self._watcher:
            self._watcher.stop()
    
    def _update_node_list(self) -> None:
        """Update the node list widget."""
        try:
            node_list = self.query_one("#node-list", NodeListWidget)
            node_list.update_canvas(self.canvas)
        except Exception:
            pass
    
    def _update_canvas_view(self) -> None:
        """Update the canvas view widget."""
        try:
            canvas_view = self.query_one("#canvas-view", CanvasViewWidget)
            canvas_view.update_canvas(self.canvas)
        except Exception:
            pass
    
    def _update_node_detail(self, node: Optional[CanvasNode]) -> None:
        """Update the node detail widget."""
        try:
            detail = self.query_one("#node-detail", NodeDetailWidget)
            detail.update_node(node)
        except Exception:
            pass
    
    def _start_watcher(self) -> None:
        """Start watching the file for changes."""
        from watchdog.observers import Observer
        from watchdog.events import FileSystemEventHandler, FileModifiedEvent
        
        class CanvasHandler(FileSystemEventHandler):
            def __init__(self, app: CanvasTUI):
                self.app = app
            
            def on_modified(self, event: FileModifiedEvent) -> None:
                if not event.is_directory and event.src_path.endswith('.canvas'):
                    try:
                        self.app.canvas = CanvasParser.load(event.src_path)
                        self.app.call_from_thread(self.app._refresh_views)
                    except Exception:
                        pass
        
        if self.file_path:
            handler = CanvasHandler(self)
            self._watcher = Observer()
            self._watcher.schedule(handler, str(self.file_path.parent), recursive=False)
            self._watcher.start()
    
    def _refresh_views(self) -> None:
        """Refresh all views after file change."""
        self._update_node_list()
        self._update_canvas_view()
        if self.current_node:
            self.current_node = self.canvas.get_node_by_id(self.current_node.node_id)
            self._update_node_detail(self.current_node)
    
    def action_search(self) -> None:
        """Open search widget."""
        try:
            search = self.query_one("#search-widget", SearchWidget)
            search.toggle()
        except Exception:
            pass
    
    def action_new_node(self) -> None:
        """Create a new node."""
        # TODO: Implement node creation dialog
        self.notify("Node creation coming soon!", title="Info")
    
    def action_edit(self) -> None:
        """Edit the current node."""
        if self.current_node:
            # TODO: Implement node editing
            self.notify("Node editing coming soon!", title="Info")
        else:
            self.notify("No node selected", title="Warning", severity="warning")
    
    def action_delete(self) -> None:
        """Delete the current node."""
        if self.current_node:
            # TODO: Implement node deletion with confirmation
            self.notify("Node deletion coming soon!", title="Info")
        else:
            self.notify("No node selected", title="Warning", severity="warning")
    
    def action_toggle_watch(self) -> None:
        """Toggle file watching."""
        self.is_watching = not self.is_watching
        status = "enabled" if self.is_watching else "disabled"
        self.notify(f"File watching {status}", title="Watch Mode")
        
        if self.is_watching and self.file_path and not self._watcher:
            self._start_watcher()
        elif not self.is_watching and self._watcher:
            self._watcher.stop()
            self._watcher = None
    
    def action_help(self) -> None:
        """Show help dialog."""
        self.notify("Press Q to quit, S to search, N for new node", title="Help")
    
    def action_next_node(self) -> None:
        """Select the next node."""
        try:
            node_list = self.query_one("#node-list", NodeListWidget)
            node_list.select_next()
        except Exception:
            pass
    
    def action_prev_node(self) -> None:
        """Select the previous node."""
        try:
            node_list = self.query_one("#node-list", NodeListWidget)
            node_list.select_previous()
        except Exception:
            pass
    
    def action_select_node(self) -> None:
        """Select the current node."""
        try:
            node_list = self.query_one("#node-list", NodeListWidget)
            node = node_list.get_selected_node()
            if node:
                self.current_node = node
                self._update_node_detail(node)
        except Exception:
            pass
    
    def action_clear_selection(self) -> None:
        """Clear the current selection."""
        self.current_node = None
        self._update_node_detail(None)
    
    def on_node_list_widget_node_selected(self, event: NodeListWidget.NodeSelected) -> None:
        """Handle node selection from the list."""
        self.current_node = event.node
        self._update_node_detail(event.node)
    
    def on_search_widget_search(self, event: SearchWidget.Search) -> None:
        """Handle search event."""
        self.search_query = event.query
        results = self.canvas.search_nodes(event.query)
        
        try:
            node_list = self.query_one("#node-list", NodeListWidget)
            node_list.show_search_results(results)
        except Exception:
            pass
        
        self.notify(f"Found {len(results)} node(s)", title="Search")
