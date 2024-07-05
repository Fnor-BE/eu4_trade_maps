from functools import reduce
import files
import numpy as np
import pandas as pd
from PIL import Image, ImageOps
import colorsys

nodes = files.load_nodes()
edges = files.load_edges()
distances = files.load_distances()


def norm(s: pd.Series) -> pd.Series:
    # why is this not innate?
    return s/s.max()


def reach(node: str) -> pd.Series:
    '''The nodes which can reach this node, with the number of steps to reach
    as the values.'''
    col = distances[node]
    return col.loc[col < np.inf]


def filename(node: str) -> str:
    return f'raw_maps/nodes/{node}.png'


def img_colorof(img: Image) -> tuple:
    # PNG format has palette naturally. Our images only contain a single main
    # colors with the rest transparent.
    for _, rgba in img.getcolors():
        r, g, b, a = rgba
        if a >= 128:
            return r, g, b
    raise


images = {node: Image.open(filename(node)) for node in nodes}


def find_node_colors() -> pd.DataFrame:
    """Finds the main colors of all node images.
    Warning: may take a few seconds."""
    return pd.DataFrame(
        [img_colorof(img) for img in images.values()],
        index=nodes, columns=['r', 'g', 'b']
    )


try:
    node_colors = files.load_node_colors()
except:
    node_colors = find_node_colors()
    files.write_node_colors(node_colors)


def colormap(node: str) -> pd.Series:
    reach_nodes = reach(node)
    saturations = norm(reach_nodes.max() - reach_nodes + 1)
    r, g, b = node_colors.loc[node]
    h, l, _ = colorsys.rgb_to_hls(r / 255, g / 255, b / 255)

    def saturation_map(s: float):
        return colorsys.hls_to_rgb(h, l, s)

    colors = saturations.apply(saturation_map)
    return colors


def b2a(img: Image) -> Image:
    """Converts rgb to rgba by treating all black pixels as transparent, leaving
    rest as fully opaque.

    For performance, assumes red == 0 as black."""
    rgba = img.convert("RGBA")
    arr = np.array(rgba)
    # any channel>0: not black. False=0, True=1. ubyte=8bit. 255 is max(ubyte)
    arr_alpha = np.any(arr[:, :, :3] > 0, axis=2).astype(np.ubyte) * 255
    alpha = Image.fromarray(arr_alpha, mode="L")
    rgba.putalpha(alpha)
    return rgba


def complete(node: str) -> Image:
    cmap = colormap(node).to_dict()

    def make_img(node, rgb):
        r, g, b = rgb
        mask = images[node].split()[-1]
        arr = np.uint8(np.array(mask))
        full = np.uint8(np.expand_dims(arr, axis=2) * np.array([r, g, b, 1.]))
        return full

    return Image.fromarray(sum((
        make_img(node, rgb) for node, rgb in cmap.items()
    )))


def save_only_node(node: str) -> None:
    print(f'creating {node}...')
    img = complete(node)
    print('saving...')
    img.save(f'export/only_nodes/{node}.png')
    print(f'saved to export/only_nodes/{node}.png')


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == 'colors':
            node_colors = find_node_colors()
            files.write_node_colors(node_colors)

    for node in nodes:
        save_only_node(node)
    # complete('genua').show()
