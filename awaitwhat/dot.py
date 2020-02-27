import json

from .graph import vertices_and_edges


def label(vertex):
    label = f"{vertex.name} {vertex.state or ''}\n{vertex.traceback or ''}"
    label = json.dumps(label).replace("\\n", r"\l")
    return f"[label={label}]"


def dumps(tasks):
    """
    Renders Task dependency graph in graphviz format.
    Returns a string.
    """

    prefix = "\n        "

    vertices, edges = vertices_and_edges(tasks)
    node_labels = prefix.join(
        f"{id(vertex.task)} {label(vertex)}" for vertex in vertices
    )
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
