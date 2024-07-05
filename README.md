This is a simple tool for making visualizations of trade nodes in the game Europa Universalis IV.

I wrote this code to help with making the images in this album

https://imgur.com/gallery/eu4-trade-node-ranges-1-31-5-16bUV5Y

You need Python with write permissions and the NumPy, Pandas, PIL, and colorsys libraries, the 00_tradenodes.txt file from the eu4 game files, and the individual base images of every individual trade node.
You can get a base image using F10 while using the trade node mapmode. I used GIMP with color select plus some manual separation to extract a separate image for every trade node.

The code works as follows:
The `files` module just makes sure the other modules are working on the right files.
`parse` parses the 00_tradenodes.txt paradox file for the edges between all trade nodes, and creates the edges.txt intermediate file.
`distances` then interprets that graph to produce the shortest distance matrix. I think I got the algo from stackoverflow somewhere, should've kept the link.
`nodes` actually makes the core images of each of the trade nodes, using the correct saturation etc. These are still just only the trade nodes though.
`tmp` is a crude hack to add transparency, for the next step.
`pretty` adds backgrounds. The bg_wl image is easily made out of the F10 mapmode screenshot with some wasteland-gray color fill after having extracted all trade nodes.

If you use this code, please credit me.

Note: downloader beware, I haven't ran this since 2021. It worked once, then, for me. Nothing else is guaranteed.
