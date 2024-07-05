"""
converts the only_nodes exports from rgb to rgba by converting black pixels to
transparent. Yes it's a hack but job's done now.
"""
import os
import numpy as np
import pandas as pd
from PIL import Image, ImageEnhance
from nodes import b2a

folder = 'export/only_nodes'


def fname(node):
    return folder + f'/{node}.png'


nodes = [name[:-4] for name in os.listdir(folder)]

images = {node: Image.open(fname(node)) for node in nodes}


for node, image in images.items():
    rgba = b2a(image)
    rgba.save(fname(node))
