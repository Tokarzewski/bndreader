import bndreader, os
import networkx as nx
import matplotlib.pyplot as plt

filepath1 = "Boiler_Convector.bnd"
filepath2 = "DOAS_Preheat.bnd"
filepath3 = "FCU_Boiler_Chiller.bnd"
filepath4 = "PTHP.bnd"

G = bndreader.Graph(filepath3)
#print(G.edges)
nx.draw(G)
plt.savefig('graph_image.png')
os.startfile('graph_image.png')