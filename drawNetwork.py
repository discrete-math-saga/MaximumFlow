import networkx as nx
import matplotlib.pyplot as plt
from typing import NamedTuple

class Point(NamedTuple):
    x:float
    y:float

def drawNetwork(G:nx.DiGraph, position:dict[str,Point],
                font_size=20, node_size=1000, edge_width=1, node_color='c',arrowsize=10, withFlow=False) -> None:
    fig,ax =plt.subplots(figsize=(8,8))
    nx.draw_networkx_nodes(G, position, node_size=node_size,node_color=node_color)
    nx.draw_networkx_labels(G, position, font_size = font_size)
    nx.draw_networkx_edges(G, position, width = edge_width,
        arrows = True, arrowsize = arrowsize ,node_size = node_size)
    edgeLabels:dict[tuple[str,str],str] = dict()
    for u,v in G.edges:
        weight = G.edges[u,v]['weight']
        if withFlow:
            flow = G.edges[u,v]['flow']
            edgeLabels[u,v]=f'{flow}/{weight}'
        else:
            edgeLabels[u,v]=f'{weight}'
    nx.draw_networkx_edge_labels(G, position, 
        edge_labels = edgeLabels, font_size = font_size) 
    ax.set_axis_off()