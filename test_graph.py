import bndreader
import networkx as nx
from networkx.readwrite import json_graph
from json import dump

filepath1 = "files\Boiler_Convector.bnd"
filepath2 = "files\DOAS_Preheat.bnd"
filepath3 = "files\FCU_Boiler_Chiller.bnd"
filepath4 = "files\PTHP.bnd"

filepaths = [filepath1,filepath2,filepath3,filepath4]

for filepath in filepaths:
    bnd = bndreader.parser(filepath)
    bnd.save_bnd_as_json(filepath)
    bnd.graph_image(filepath, open=True)

bnd = bndreader.parser(filepath2)
G = bnd.graph()

with open('files\\Graph.json', 'w+') as file:
    dump(json_graph.node_link_data(G), file, indent=4)