from dataclasses import dataclass
A = False
B = True


@dataclass
class Node:
    attributes: list
    type: bool
