"""
Parses the nodes and the edges between them from paradox's data file.
File is eu4/common/00_tradenodes.txt, user should copy it to local folder.
Edges are in incoming - outgoing order.
"""

import files
import numpy as np
from typing import Set, Tuple


def parse_00_tradenodes(text: str):
    class Node:
        def __init__(self, name: str) -> None:
            self.name = name
            self.inland = False
            self.out = set()

        def __repr__(self):
            return f'Node(name=\'{self.name}\', out={self.out})'

    nodes_parse = {}
    current_node = None
    in_members = False
    in_outgoing = False

    for i, line in enumerate(text):
        try:
            if not line.startswith('\t'):
                if line == '}\n':
                    nodes_parse[current_node.name] = current_node
                else:
                    current_node = Node(line.split('=')[0])
                continue

            assert current_node is not None

            if line.startswith('\tlocation='):
                current_node.location = line.split('=')[1].strip()
                continue

            if line == '\tinland=yes\n':
                current_node.inland = True
                continue

            if in_outgoing:
                if 'name' in line:
                    current_node.out.add(line.split('\"')[1])
                elif line == '\t}\n':
                    in_outgoing = False
                continue
            elif line == '\toutgoing={\n':
                in_outgoing = True
                continue

            if in_members:
                current_node.provinces = set(
                    int(x) for x in line.strip().split()
                )
                in_members = False
            elif line == '\tmembers={\n':
                in_members = True

        except:
            print(f"error at line {i}")
            print(line)
            raise

    nodes: Set[str] = set(nodes_parse.keys())

    edges: Set[Tuple[str, str]] = set()

    for name, node in nodes_parse.items():
        edges |= set(tuple([name, out_node]) for out_node in node.out)

    return nodes, edges


if __name__ == "__main__":
    nodes, edges = parse_00_tradenodes(files.load_tradenodes())

    files.write_nodes(nodes)
    files.write_edges(edges)
