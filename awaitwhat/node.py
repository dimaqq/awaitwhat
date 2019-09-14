from dataclasses import dataclass

@dataclass
class Node:
    name: str
    state: str
    traceback: str
    task: str = None


