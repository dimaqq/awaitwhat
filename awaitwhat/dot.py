import json

from .node import vertices_and_edges


def label(node):
    label = f"{node.name} {node.state or ''}\n{node.traceback or ''}"
    label = json.dumps(label).replace("\\n", r"\l")
    return f"[label={label}]"


def dumps(tasks):
    """
    Renders Task dependency graph in graphviz format.
    Returns a string.
    """

    prefix = "\n        "

    vertices, edges = vertices_and_edges(tasks)
    node_labels = prefix.join(f"{id(node.task)} {label(node)}" for node in vertices)
    edge_labels = prefix.join(
        f"{id(edge.src.task)} -> {id(edge.dst.task)}" for edge in edges
    )

    return f"""
    digraph {{
        node [shape="note", fontname="Courier New"];
        {node_labels}
        {edge_labels}
    }}
    """.strip()
