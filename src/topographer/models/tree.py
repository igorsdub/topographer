from __future__ import annotations

"""Core tree-shaped result models used across Topographer algorithms."""

from dataclasses import dataclass, field
from typing import Any

import networkx as nx


@dataclass(slots=True)
class SplitTree:
    """Result container for split-tree computation."""

    graph: nx.Graph
    root: Any | None
    critical_nodes: list[Any]
    scalar: str
    augmented: bool = False
    arc_vertices: dict[tuple[Any, Any], list[Any]] = field(default_factory=dict)
    node_metadata: dict[Any, dict[str, Any]] = field(default_factory=dict)

    @property
    def tree(self) -> nx.Graph:
        """Backward-compatible alias for ``graph``."""
        return self.graph

    @tree.setter
    def tree(self, value: nx.Graph) -> None:
        """Set the underlying graph through the ``tree`` alias."""
        self.graph = value


@dataclass(slots=True)
class JoinTree:
    """Result container for join-tree computation."""

    graph: nx.Graph
    root: Any | None
    critical_nodes: list[Any]
    scalar: str
    augmented: bool = False
    arc_vertices: dict[tuple[Any, Any], list[Any]] = field(default_factory=dict)
    node_metadata: dict[Any, dict[str, Any]] = field(default_factory=dict)

    @property
    def tree(self) -> nx.Graph:
        """Backward-compatible alias for ``graph``."""
        return self.graph

    @tree.setter
    def tree(self, value: nx.Graph) -> None:
        """Set the underlying graph through the ``tree`` alias."""
        self.graph = value


@dataclass(slots=True)
class ContourTree:
    """Result container for contour-tree computation and context."""

    graph: nx.Graph
    scalar: str
    split_tree: SplitTree | None = None
    join_tree: JoinTree | None = None
    augmented: bool = False
    critical_nodes: list[Any] = field(default_factory=list)
    arc_vertices: dict[tuple[Any, Any], list[Any]] = field(default_factory=dict)
    node_metadata: dict[Any, dict[str, Any]] = field(default_factory=dict)

    @property
    def tree(self) -> nx.Graph:
        """Backward-compatible alias for ``graph``."""
        return self.graph

    @tree.setter
    def tree(self, value: nx.Graph) -> None:
        """Set the underlying graph through the ``tree`` alias."""
        self.graph = value

    @property
    def ST(self) -> SplitTree | None:
        """Backward-compatible alias for ``split_tree``."""
        return self.split_tree

    @ST.setter
    def ST(self, value: SplitTree | None) -> None:
        """Set split-tree context through ``ST`` alias."""
        self.split_tree = value

    @property
    def JT(self) -> JoinTree | None:
        """Backward-compatible alias for ``join_tree``."""
        return self.join_tree

    @JT.setter
    def JT(self, value: JoinTree | None) -> None:
        """Set join-tree context through ``JT`` alias."""
        self.join_tree = value


# Backward-compatible aliases
SplitTreeResult = SplitTree
JoinTreeResult = JoinTree
ContourTreeResult = ContourTree
ST = SplitTree
JT = JoinTree
CT = ContourTree


__all__ = [
    "SplitTree",
    "JoinTree",
    "ContourTree",
    "SplitTreeResult",
    "JoinTreeResult",
    "ContourTreeResult",
    "ST",
    "JT",
    "CT",
]
