import networkx as nx
import matplotlib.pyplot as plt
from maxFlow import MaxFlow
from drawNetwork import drawNetwork, Point
def createNetwork()-> tuple[nx.DiGraph,dict[str,Point]]:
    nodeList=list()
    for k in range(6):
        nodeList.append(f'v{k}')
    position:dict[str,Point]={
        'v0':Point(0,0.5),'v1':Point(.3,.7),'v2':Point(.3,.3),'v3':Point(.5,.5),
        'v4':Point(.7,.7),'v5':Point(.7,.3),'v6':Point(1,.5)
    }
    edgeListWithWeight:list[tuple[str,str,float]] =[
        ('v0','v1',6), ('v0','v2', 4),
        ('v1','v2',2), ('v1','v3', 3),
        ('v2','v3',4), ('v2','v5', 4),
        ('v3','v4',4), ('v3','v5',2),
        ('v4','v1',2), ('v4','v5',3),('v4','v6',8),
        ('v5','v6',5)
    ]
    G = nx.DiGraph()
    G.add_nodes_from(nodeList)
    G.add_weighted_edges_from(edgeListWithWeight)
    flow = dict()
    for u,v in G.edges:
        flow[u,v]=0
    nx.set_edge_attributes(G, flow, 'flow')
    return G, position


def drawNetworkTex(G:nx.DiGraph, position:dict[str,Point],aux=False,withBlock=True,updatePath=[]):
    text = ''
    if withBlock:
        text += r'\begin{frame}'+'\n'
        text+=r'\begin{tikzpicture}'+'\n'
    for node in G.nodes:
        p = position[node]
        nstr = node.replace('v','v_')
        text += rf'\node[my node] ({node}) at ({p[0]},{p[1]}) {{${nstr}$}};'+'\n'
    text +='\n'
    for u,v in G.edges:
        weight = G.edges[u,v]['weight']
        color = 'black'
        if aux:
            color = 'blue'
            if G.edges[u,v]['direction']=='-':
                color = 'red'
            text += rf'\draw[->,{color}] ({u}) edge node[above] {{{weight}}} ({v});'+'\n' 
        else:
            flow = G.edges[u,v]['flow']
            text += rf'\draw[->,{color}] ({u}) edge node[above] {{{flow}/{weight}}} ({v});'+'\n' 
    if aux:    
        text +='% update path\n'
        for p,q in updatePath:
            text+=rf'\draw[->,orange!50,line width=5,opacity=.7] ({p}) -- ({q});'+'\n'
    if withBlock:
        text += r'\end{tikzpicture}'+'\n'+r'\end{frame}'+'\n'
    return text

if __name__ == '__main__':
    G, position = createNetwork()
    #drawNetworkTex(G, position)
    #drawNetwork(G, position,withFlow=True)
    sys = MaxFlow(G,'v0','v6')
    text = ''
    while sys.oneStep():
        text +=drawNetworkTex(sys.GAux,position,aux=True,updatePath=sys.updatePath)
        text += '\n'
    # sys.oneStep()
    # drawNetworkTex(sys.GAux,position,aux=True)
    # sys.findMax()
    text +=drawNetworkTex(G, position)
    with open('output.tex',mode='w') as f:
        f.write(text)
    # drawNetwork(G, position,withFlow=True)
