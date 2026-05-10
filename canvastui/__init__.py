"""
CanvasTUI - A powerful terminal-based JSON Canvas viewer and editor.

JSON Canvas is an open file format for infinite canvas data, 
popularized by Obsidian. This tool allows you to view, navigate, 
and edit .canvas files directly in your terminal.
"""

__version__ = "1.0.0"
__author__ = "gitstq"
__license__ = "MIT"

from canvastui.app import CanvasTUI
from canvastui.canvas_parser import CanvasParser, CanvasNode, CanvasEdge, CanvasFile

__all__ = [
    "CanvasTUI",
    "CanvasParser",
    "CanvasNode",
    "CanvasEdge",
    "CanvasFile",
]
