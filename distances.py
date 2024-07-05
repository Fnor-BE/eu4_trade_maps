import files
import numpy as np
import pandas as pd


def compute_distances(nodes: np.ndarray, edges: np.ndarray):
    node_count: int = len(nodes)

    # inf == not connected. default value
    distances = np.full(shape=(node_count, node_count), fill_value=np.inf)

    def node_nr(node_name: str) -> int:
        return np.argwhere(nodes == node_name)[0]

    # write down connections as 1 step apart
    for start, end in edges:
        a = node_nr(start)
        b = node_nr(end)
        distances[a, b] = 1

    # every node is distance 0 to itself
    for i in range(0, node_count):
        distances[i, i] = 0

    # if the shortest distance between two nodes is larger than the total
    # distance using a stepping stone, set the distance to equal that sum.
    # Doing this for all nodes will connect all nodes with their shortest
    # distances.
    # O(N^3)
    for k in range(0, node_count):
        for i in range(0, node_count):
            for j in range(0, node_count):
                if distances[i, j] > distances[i, k] + distances[k, j]:
                    distances[i, j] = distances[i, k] + distances[k, j]

    return pd.DataFrame(distances, index=nodes, columns=nodes, dtype=float)


if __name__ == "__main__":
    nodes = files.load_nodes()
    edges = files.load_edges()
    distances = compute_distances(nodes, edges)
    distances.to_csv('distances.csv')
