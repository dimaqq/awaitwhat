import json

from . import graph


def label(vertex):
    """ Graph vertex label in dot format """
    label = f"{vertex.name} {vertex.state or ''}\n{vertex.traceback or ''}"
    label = json.dumps(label).replace("\\n", r"\l")
    return f"[label={label}]"


def dumps(tasks):
    """
    Renders Task dependency graph in graphviz format.
    Returns a string.
    """

    prefix = "\n        "

    vertices, edges = graph.new(tasks)
    vertices = prefix.join(f"{id(vertex.task)} {label(vertex)}" for vertex in vertices)
    edges = prefix.join(f"{id(edge.src.task)} -> {id(edge.dst.task)}" for edge in edges)

    return f"""
    digraph {{
        node [shape="note", fontname="Courier New"];
        {vertices}
        {edges}
    }}
    """.strip()
