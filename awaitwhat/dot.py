import asyncio
import json
import re

from dataclasses import dataclass

from .node import Node, build_node, build_nodes_and_edges


def labelify(node):
    label = f"{node.name} {node.state or ''}\n{node.traceback or ''}"
    label = json.dumps(label).replace("\\n", r"\l")
    return f"[label={label}]"


def dumps(tasks):
    """
    Renders Task dependency graph in graphviz format.
    Returns a string.
    """

    PREFIX = '\n        '

    nodes, edges = build_nodes_and_edges(tasks)

    node_labesls = PREFIX.join(f'{id(node.task)} {labelify(node)}' for node in nodes)
    edge_labels = PREFIX.join(edges)

    return f"""
    digraph {{
        node [shape="note", fontname="Courier New"];
        {node_labesls}
        {edge_labels}
    }}
    """.strip()
