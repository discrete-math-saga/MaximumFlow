import networkx as nx
from drawNetwork import drawNetwork, Point

def createNetwork()-> tuple[nx.DiGraph,dict[str,Point]]:
    nodeList=list()
    for k in range(6):
        nodeList.append(f'v{k}')

    position:dict[str,Point]={
        'v0':Point(0,0.5),'v1':Point(.3,.7),'v2':Point(.3,.3),
        'v3':Point(.7,.7),'v4':Point(.7,.3),'v5':Point(1,.5)
    }
    edgeListWithWeight:list[tuple[str,str,float]] =[
        ('v0','v1',6), ('v0','v2', 4),
        ('v1','v2',2), ('v1','v3', 3),
        ('v2','v4',4),
        ('v3','v4',7), ('v3','v5',2),
        ('v4','v1',1), ('v4','v5',8)
    ]
    G = nx.DiGraph()
    G.add_nodes_from(nodeList)
    G.add_weighted_edges_from(edgeListWithWeight)
    flow = dict()
    for u,v in G.edges:
        flow[u,v]=0
    nx.set_edge_attributes(G, flow, 'flow')
    return G, position


if __name__ == '__main__':
    G, position = createNetwork()
    drawNetwork(G, position)
    G.edges