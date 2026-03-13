"""Validation helpers for graph-based topological computations.

These checks enforce baseline assumptions used by split/join tree,
contour tree, and persistence algorithms.
"""

import networkx as nx

from topographer.core.uniqueness import assert_unique_scalar_values


def check_graph(
    G: nx.Graph,
    scalar_attr: str = "scalar",
    require_connected: bool = True,
):
    """Validate that a graph is ready for Topographer algorithms.

    The function verifies graph type, non-emptiness, optional connectivity,
    scalar attribute presence on every node, scalar numeric type, and global
    scalar uniqueness.

    Parameters
    ----------
    G:
        Input NetworkX graph.
    scalar_attr:
        Node attribute name that stores scalar values.
    require_connected:
        If ``True``, the graph must have exactly one connected component.

    Returns
    -------
    bool
        ``True`` when all checks pass.
    """

    if not isinstance(G, nx.Graph):
        raise TypeError("Graph must be a networkx.Graph")

    if G.number_of_nodes() == 0:
        raise ValueError("Graph is empty")

    if require_connected and not nx.is_connected(G):
        raise ValueError("Graph must be connected")

    for node, data in G.nodes(data=True):
        if scalar_attr not in data:
            raise ValueError(f"Node {node} missing scalar attribute '{scalar_attr}'")

        value = data[scalar_attr]

        if not isinstance(value, (int, float)):
            raise ValueError(f"Scalar value on node {node} must be numeric")

    assert_unique_scalar_values(G, scalar_attr=scalar_attr)

    return True
