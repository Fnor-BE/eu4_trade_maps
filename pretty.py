import os
from PIL import Image, ImageEnhance

bg = Image.open('raw_maps/bg_wl.png')

nodes = [name[:-4] for name in os.listdir('export/only_nodes')]

images = {node: Image.open(f'export/only_nodes/{node}.png') for node in nodes}

bg_dark = ImageEnhance.Brightness(bg).enhance(0.5)


def add_bg(node: str):
    img = images[node].copy()
    bgc = bg.copy()
    bgc.paste(img, (0, 0), img.split()[-1])
    return bgc


for node in nodes:
    print(f'creating {node}...')
    final = add_bg(node)
    print('saving...')
    fname = f'export/final/{node}.png'
    final.save(fname)
    print(f'saved to {fname}.')
