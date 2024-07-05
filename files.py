"""
Helps loading and writing to common data files.
"""
import numpy as np
from numpy.core.defchararray import index
import pandas as pd
from typing import List

tradenodestxt_filename: str = '00_tradenodes.txt'
nodes_filename: str = 'nodes.txt'
edges_filename: str = 'edges.txt'
distances_filename: str = 'distances.csv'
node_colors_filename: str = 'node_colors.csv'


def _write_setarray(filename: str, maybe_set) -> None:
    # parse.py produces sets, not ndarrays, so we convert them if necessary
    if not isinstance(maybe_set, np.ndarray):
        maybe_set = np.array(list(maybe_set))
    np.savetxt(filename, maybe_set, fmt='%s')


def _write_df(filename: str, df: pd.DataFrame) -> None:
    df.to_csv(filename)


def _load_df(filename: str) -> pd.DataFrame:
    return pd.read_csv(filename, index_col=0)


def load_tradenodes() -> List[str]:
    with open(tradenodestxt_filename, 'r') as f:
        return f.readlines()


def write_nodes(nodes):
    _write_setarray(nodes_filename, nodes)


def load_nodes() -> np.ndarray:
    return np.loadtxt(nodes_filename, dtype=str)


def write_edges(edges) -> None:
    _write_setarray(edges_filename, edges)


def load_edges() -> np.ndarray:
    return np.loadtxt(edges_filename, dtype=str)


def write_distances(distances: pd.DataFrame) -> None:
    _write_df(distances_filename, distances)


def load_distances() -> pd.DataFrame:
    return _load_df(distances_filename)


def write_node_colors(node_colors: pd.DataFrame):
    _write_df(node_colors_filename, node_colors)


def load_node_colors() -> pd.DataFrame:
    return _load_df(node_colors_filename)
