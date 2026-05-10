"""
Canvas file parser for JSON Canvas format.

This module provides classes for parsing, validating, and manipulating
JSON Canvas (.canvas) files used by Obsidian and other applications.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

from pydantic import BaseModel, Field, field_validator


class NodeType(str, Enum):
    """Types of nodes in a JSON Canvas."""
    TEXT = "text"
    FILE = "file"
    LINK = "link"
    GROUP = "group"


class NodeSide(str, Enum):
    """Sides of a node for edge connections."""
    TOP = "top"
    BOTTOM = "bottom"
    LEFT = "left"
    RIGHT = "right"


@dataclass
class CanvasNode:
    """
    Represents a node in a JSON Canvas.
    
    Nodes can be text, file references, links, or groups.
    """
    node_id: str
    node_type: NodeType
    x: int
    y: int
    width: int
    height: int
    text: str = ""
    file: str = ""
    url: str = ""
    color: str = ""
    label: str = ""
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CanvasNode:
        """Create a CanvasNode from a dictionary."""
        node_type = NodeType(data.get("type", "text"))
        return cls(
            node_id=data.get("id", ""),
            node_type=node_type,
            x=data.get("x", 0),
            y=data.get("y", 0),
            width=data.get("width", 250),
            height=data.get("height", 140),
            text=data.get("text", ""),
            file=data.get("file", ""),
            url=data.get("url", ""),
            color=data.get("color", ""),
            label=data.get("label", ""),
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert the node to a dictionary."""
        result: dict[str, Any] = {
            "id": self.node_id,
            "type": self.node_type.value,
            "x": self.x,
            "y": self.y,
            "width": self.width,
            "height": self.height,
        }
        if self.text:
            result["text"] = self.text
        if self.file:
            result["file"] = self.file
        if self.url:
            result["url"] = self.url
        if self.color:
            result["color"] = self.color
        if self.label:
            result["label"] = self.label
        return result


@dataclass
class CanvasEdge:
    """
    Represents an edge (connection) between two nodes.
    
    Edges can have labels and connect specific sides of nodes.
    """
    edge_id: str
    from_node: str
    from_side: NodeSide = NodeSide.RIGHT
    to_node: str = ""
    to_side: NodeSide = NodeSide.LEFT
    label: str = ""
    color: str = ""
    
    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> CanvasEdge:
        """Create a CanvasEdge from a dictionary."""
        return cls(
            edge_id=data.get("id", ""),
            from_node=data.get("fromNode", ""),
            from_side=NodeSide(data.get("fromSide", "right")),
            to_node=data.get("toNode", ""),
            to_side=NodeSide(data.get("toSide", "left")),
            label=data.get("label", ""),
            color=data.get("color", ""),
        )
    
    def to_dict(self) -> dict[str, Any]:
        """Convert the edge to a dictionary."""
        result: dict[str, Any] = {
            "id": self.edge_id,
            "fromNode": self.from_node,
            "fromSide": self.from_side.value,
            "toNode": self.to_node,
            "toSide": self.to_side.value,
        }
        if self.label:
            result["label"] = self.label
        if self.color:
            result["color"] = self.color
        return result


@dataclass
class CanvasFile:
    """
    Represents a complete JSON Canvas file.
    
    Contains nodes, edges, and metadata.
    """
    nodes: list[CanvasNode] = field(default_factory=list)
    edges: list[CanvasEdge] = field(default_factory=list)
    file_path: Path | None = None
    
    @property
    def node_count(self) -> int:
        """Return the number of nodes."""
        return len(self.nodes)
    
    @property
    def edge_count(self) -> int:
        """Return the number of edges."""
        return len(self.edges)
    
    @property
    def bounds(self) -> tuple[int, int, int, int]:
        """Return the bounding box (min_x, min_y, max_x, max_y)."""
        if not self.nodes:
            return (0, 0, 0, 0)
        
        min_x = min(n.x for n in self.nodes)
        min_y = min(n.y for n in self.nodes)
        max_x = max(n.x + n.width for n in self.nodes)
        max_y = max(n.y + n.height for n in self.nodes)
        
        return (min_x, min_y, max_x, max_y)
    
    def get_node_by_id(self, node_id: str) -> CanvasNode | None:
        """Get a node by its ID."""
        for node in self.nodes:
            if node.node_id == node_id:
                return node
        return None
    
    def get_edges_for_node(self, node_id: str) -> list[CanvasEdge]:
        """Get all edges connected to a node."""
        return [
            edge for edge in self.edges
            if edge.from_node == node_id or edge.to_node == node_id
        ]
    
    def get_connected_nodes(self, node_id: str) -> list[CanvasNode]:
        """Get all nodes connected to a given node."""
        connected_ids = set()
        for edge in self.edges:
            if edge.from_node == node_id:
                connected_ids.add(edge.to_node)
            elif edge.to_node == node_id:
                connected_ids.add(edge.from_node)
        
        return [
            node for node in self.nodes
            if node.node_id in connected_ids
        ]
    
    def search_nodes(self, query: str) -> list[CanvasNode]:
        """Search nodes by text content."""
        query_lower = query.lower()
        return [
            node for node in self.nodes
            if query_lower in node.text.lower()
            or query_lower in node.label.lower()
            or query_lower in node.file.lower()
        ]


class CanvasParser:
    """
    Parser for JSON Canvas files.
    
    Handles loading, validating, and saving .canvas files.
    """
    
    @staticmethod
    def load(file_path: Path | str) -> CanvasFile:
        """
        Load a canvas file from disk.
        
        Args:
            file_path: Path to the .canvas file
            
        Returns:
            CanvasFile object with parsed data
            
        Raises:
            FileNotFoundError: If the file doesn't exist
            json.JSONDecodeError: If the file isn't valid JSON
            ValueError: If the file format is invalid
        """
        path = Path(file_path)
        
        if not path.exists():
            raise FileNotFoundError(f"Canvas file not found: {path}")
        
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return CanvasParser.parse(data, path)
    
    @staticmethod
    def parse(data: dict[str, Any], file_path: Path | None = None) -> CanvasFile:
        """
        Parse canvas data from a dictionary.
        
        Args:
            data: Dictionary containing canvas data
            file_path: Optional path to the source file
            
        Returns:
            CanvasFile object with parsed data
        """
        nodes = [
            CanvasNode.from_dict(node_data)
            for node_data in data.get("nodes", [])
        ]
        
        edges = [
            CanvasEdge.from_dict(edge_data)
            for edge_data in data.get("edges", [])
        ]
        
        return CanvasFile(nodes=nodes, edges=edges, file_path=file_path)
    
    @staticmethod
    def save(canvas: CanvasFile, file_path: Path | str | None = None) -> None:
        """
        Save a canvas file to disk.
        
        Args:
            canvas: CanvasFile to save
            file_path: Path to save to (uses canvas.file_path if not provided)
        """
        path = Path(file_path) if file_path else canvas.file_path
        
        if path is None:
            raise ValueError("No file path specified for saving")
        
        data = CanvasParser.to_dict(canvas)
        
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    
    @staticmethod
    def to_dict(canvas: CanvasFile) -> dict[str, Any]:
        """
        Convert a CanvasFile to a dictionary.
        
        Args:
            canvas: CanvasFile to convert
            
        Returns:
            Dictionary representation of the canvas
        """
        return {
            "nodes": [node.to_dict() for node in canvas.nodes],
            "edges": [edge.to_dict() for edge in canvas.edges],
        }
    
    @staticmethod
    def create_empty() -> CanvasFile:
        """Create an empty canvas file."""
        return CanvasFile()
