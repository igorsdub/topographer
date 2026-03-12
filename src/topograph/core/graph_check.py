import networkx as nx


def check_graph(
    G: nx.Graph,
    scalar_attr: str = "scalar",
    require_connected: bool = True,
):
    """
    Validate graph and scalar attribute for TopoGraph algorithms.

    Only implements minimal checks needed for tests.
    """

    if not isinstance(G, nx.Graph):
        raise TypeError("Graph must be a networkx.Graph")

    if G.number_of_nodes() == 0:
        raise ValueError("Graph is empty")

    if require_connected and not nx.is_connected(G):
        raise ValueError("Graph must be connected")

    values = []

    for node, data in G.nodes(data=True):
        if scalar_attr not in data:
            raise ValueError(f"Node {node} missing scalar attribute '{scalar_attr}'")

        value = data[scalar_attr]

        if not isinstance(value, (int, float)):
            raise ValueError(f"Scalar value on node {node} must be numeric")

        values.append(value)

    if len(values) != len(set(values)):
        raise ValueError("Duplicate scalar values detected")

    return True
