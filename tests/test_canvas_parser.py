"""
Test suite for CanvasTUI.
"""

import pytest
from pathlib import Path
import tempfile
import json

from canvastui.canvas_parser import (
    CanvasParser,
    CanvasFile,
    CanvasNode,
    CanvasEdge,
    NodeType,
    NodeSide,
)


class TestCanvasNode:
    """Tests for CanvasNode class."""
    
    def test_create_text_node(self):
        """Test creating a text node."""
        node = CanvasNode(
            node_id="test-123",
            node_type=NodeType.TEXT,
            x=100,
            y=200,
            width=250,
            height=140,
            text="Hello World"
        )
        
        assert node.node_id == "test-123"
        assert node.node_type == NodeType.TEXT
        assert node.x == 100
        assert node.y == 200
        assert node.text == "Hello World"
    
    def test_node_from_dict(self):
        """Test creating a node from a dictionary."""
        data = {
            "id": "node-1",
            "type": "text",
            "x": 0,
            "y": 0,
            "width": 300,
            "height": 200,
            "text": "Test content",
            "color": "red"
        }
        
        node = CanvasNode.from_dict(data)
        
        assert node.node_id == "node-1"
        assert node.node_type == NodeType.TEXT
        assert node.text == "Test content"
        assert node.color == "red"
    
    def test_node_to_dict(self):
        """Test converting a node to a dictionary."""
        node = CanvasNode(
            node_id="node-2",
            node_type=NodeType.FILE,
            x=50,
            y=50,
            width=250,
            height=140,
            file="test.md"
        )
        
        data = node.to_dict()
        
        assert data["id"] == "node-2"
        assert data["type"] == "file"
        assert data["file"] == "test.md"
        assert "text" not in data  # Empty text should not be included


class TestCanvasEdge:
    """Tests for CanvasEdge class."""
    
    def test_create_edge(self):
        """Test creating an edge."""
        edge = CanvasEdge(
            edge_id="edge-1",
            from_node="node-a",
            from_side=NodeSide.RIGHT,
            to_node="node-b",
            to_side=NodeSide.LEFT,
            label="connects to"
        )
        
        assert edge.edge_id == "edge-1"
        assert edge.from_node == "node-a"
        assert edge.to_node == "node-b"
        assert edge.label == "connects to"
    
    def test_edge_from_dict(self):
        """Test creating an edge from a dictionary."""
        data = {
            "id": "edge-2",
            "fromNode": "node-1",
            "fromSide": "bottom",
            "toNode": "node-2",
            "toSide": "top"
        }
        
        edge = CanvasEdge.from_dict(data)
        
        assert edge.edge_id == "edge-2"
        assert edge.from_side == NodeSide.BOTTOM
        assert edge.to_side == NodeSide.TOP
    
    def test_edge_to_dict(self):
        """Test converting an edge to a dictionary."""
        edge = CanvasEdge(
            edge_id="edge-3",
            from_node="a",
            to_node="b"
        )
        
        data = edge.to_dict()
        
        assert data["id"] == "edge-3"
        assert data["fromNode"] == "a"
        assert data["toNode"] == "b"


class TestCanvasFile:
    """Tests for CanvasFile class."""
    
    def test_empty_canvas(self):
        """Test creating an empty canvas."""
        canvas = CanvasFile()
        
        assert canvas.node_count == 0
        assert canvas.edge_count == 0
        assert canvas.bounds == (0, 0, 0, 0)
    
    def test_canvas_with_nodes(self):
        """Test canvas with nodes."""
        nodes = [
            CanvasNode("n1", NodeType.TEXT, 0, 0, 100, 100, text="A"),
            CanvasNode("n2", NodeType.TEXT, 200, 200, 100, 100, text="B"),
        ]
        canvas = CanvasFile(nodes=nodes)
        
        assert canvas.node_count == 2
        bounds = canvas.bounds
        assert bounds[0] == 0  # min_x
        assert bounds[1] == 0  # min_y
        assert bounds[2] == 300  # max_x (200 + 100)
        assert bounds[3] == 300  # max_y (200 + 100)
    
    def test_get_node_by_id(self):
        """Test getting a node by ID."""
        nodes = [
            CanvasNode("node-1", NodeType.TEXT, 0, 0, 100, 100),
            CanvasNode("node-2", NodeType.TEXT, 100, 100, 100, 100),
        ]
        canvas = CanvasFile(nodes=nodes)
        
        found = canvas.get_node_by_id("node-1")
        assert found is not None
        assert found.node_id == "node-1"
        
        not_found = canvas.get_node_by_id("node-999")
        assert not_found is None
    
    def test_search_nodes(self):
        """Test searching nodes."""
        nodes = [
            CanvasNode("n1", NodeType.TEXT, 0, 0, 100, 100, text="Hello World"),
            CanvasNode("n2", NodeType.TEXT, 0, 0, 100, 100, text="Goodbye"),
            CanvasNode("n3", NodeType.TEXT, 0, 0, 100, 100, text="hello again"),
        ]
        canvas = CanvasFile(nodes=nodes)
        
        results = canvas.search_nodes("hello")
        assert len(results) == 2
        
        results = canvas.search_nodes("WORLD")
        assert len(results) == 1


class TestCanvasParser:
    """Tests for CanvasParser class."""
    
    def test_parse_dict(self):
        """Test parsing canvas data from a dictionary."""
        data = {
            "nodes": [
                {
                    "id": "node-1",
                    "type": "text",
                    "x": 0,
                    "y": 0,
                    "width": 250,
                    "height": 140,
                    "text": "Test node"
                }
            ],
            "edges": []
        }
        
        canvas = CanvasParser.parse(data)
        
        assert canvas.node_count == 1
        assert canvas.edge_count == 0
        assert canvas.nodes[0].text == "Test node"
    
    def test_save_and_load(self):
        """Test saving and loading a canvas file."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.canvas', delete=False) as f:
            temp_path = Path(f.name)
        
        try:
            # Create and save
            nodes = [
                CanvasNode("n1", NodeType.TEXT, 0, 0, 250, 140, text="Node 1"),
                CanvasNode("n2", NodeType.TEXT, 200, 200, 250, 140, text="Node 2"),
            ]
            edges = [
                CanvasEdge("e1", "n1", NodeSide.RIGHT, "n2", NodeSide.LEFT)
            ]
            canvas = CanvasFile(nodes=nodes, edges=edges, file_path=temp_path)
            
            CanvasParser.save(canvas, temp_path)
            
            # Load and verify
            loaded = CanvasParser.load(temp_path)
            
            assert loaded.node_count == 2
            assert loaded.edge_count == 1
            assert loaded.nodes[0].text == "Node 1"
            assert loaded.edges[0].from_node == "n1"
        finally:
            temp_path.unlink(missing_ok=True)
    
    def test_load_nonexistent_file(self):
        """Test loading a file that doesn't exist."""
        with pytest.raises(FileNotFoundError):
            CanvasParser.load("/nonexistent/path/file.canvas")
    
    def test_create_empty(self):
        """Test creating an empty canvas."""
        canvas = CanvasParser.create_empty()
        
        assert canvas.node_count == 0
        assert canvas.edge_count == 0


class TestCanvasIntegration:
    """Integration tests for canvas operations."""
    
    def test_connected_nodes(self):
        """Test getting connected nodes."""
        nodes = [
            CanvasNode("a", NodeType.TEXT, 0, 0, 100, 100),
            CanvasNode("b", NodeType.TEXT, 200, 0, 100, 100),
            CanvasNode("c", NodeType.TEXT, 400, 0, 100, 100),
        ]
        edges = [
            CanvasEdge("e1", "a", NodeSide.RIGHT, "b", NodeSide.LEFT),
            CanvasEdge("e2", "b", NodeSide.RIGHT, "c", NodeSide.LEFT),
        ]
        canvas = CanvasFile(nodes=nodes, edges=edges)
        
        # Node 'a' should be connected to 'b'
        connected = canvas.get_connected_nodes("a")
        assert len(connected) == 1
        assert connected[0].node_id == "b"
        
        # Node 'b' should be connected to both 'a' and 'c'
        connected = canvas.get_connected_nodes("b")
        assert len(connected) == 2
        
        # Node 'c' should be connected to 'b'
        connected = canvas.get_connected_nodes("c")
        assert len(connected) == 1
        assert connected[0].node_id == "b"
    
    def test_edges_for_node(self):
        """Test getting edges for a specific node."""
        nodes = [
            CanvasNode("x", NodeType.TEXT, 0, 0, 100, 100),
            CanvasNode("y", NodeType.TEXT, 200, 0, 100, 100),
        ]
        edges = [
            CanvasEdge("e1", "x", NodeSide.RIGHT, "y", NodeSide.LEFT, label="test"),
        ]
        canvas = CanvasFile(nodes=nodes, edges=edges)
        
        node_edges = canvas.get_edges_for_node("x")
        assert len(node_edges) == 1
        assert node_edges[0].label == "test"
