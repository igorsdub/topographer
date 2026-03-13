from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

import networkx as nx


@dataclass(slots=True)
class ContourTreeResult:
    tree: nx.Graph
    scalar: str
    augmented: bool = False
    critical_nodes: list[Any] = field(default_factory=list)
    arc_vertices: dict[tuple[Any, Any], list[Any]] = field(default_factory=dict)


__all__ = ["ContourTreeResult"]
