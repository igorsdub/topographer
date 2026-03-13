from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import networkx as nx


@dataclass(slots=True)
class SplitTreeResult:
    tree: nx.Graph
    root: Any | None
    critical_nodes: list[Any]
    scalar: str
    augmented: bool = False
    arc_vertices: dict[tuple[Any, Any], list[Any]] = field(default_factory=dict)


@dataclass(slots=True)
class JoinTreeResult:
    tree: nx.Graph
    root: Any | None
    critical_nodes: list[Any]
    scalar: str
    augmented: bool = False
    arc_vertices: dict[tuple[Any, Any], list[Any]] = field(default_factory=dict)


__all__ = ["SplitTreeResult", "JoinTreeResult"]
