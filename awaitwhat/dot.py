import json

from .node import build_nodes_and_edges


def labelify_node(node):
    label = f"{node.name} {node.state or ''}\n{node.traceback or ''}"
    label = json.dumps(label).replace("\\n", r"\l")
    return f"[label={label}]"


def dumps(tasks):
    """
    Renders Task dependency graph in graphviz format.
    Returns a string.
    """

    prefix = '\n        '

    nodes, edges = build_nodes_and_edges(tasks)
    node_labesls = prefix.join(
        f'{id(node.task)} {labelify_node(node)}' for node in nodes
    )
    edge_labels = prefix.join(edges)

    return f"""
    digraph {{
        node [shape="note", fontname="Courier New"];
        {node_labesls}
        {edge_labels}
    }}
    """.strip()
