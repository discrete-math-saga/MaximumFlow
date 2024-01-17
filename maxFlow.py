import networkx as nx

class MaxFlow:
    """
    Finding the maximum Flow on the network
    """
    def __init__(self, G:nx.DiGraph,src:str,dst:str):
        """
        Parameters
        ------
        G: the directed graph
        src: the name of the source node
        dst: the name of the destination node
        """
        self._G = G
        self._src = src
        self._dst = dst
        self._createAux()

    def _findPathSub(self,A:list[tuple[str,str]])->list[tuple[str,str]]:
        """
        Return the path from the list of used edges
        """
        A.reverse()
        P: list[tuple[str, str]] = [A[0]]
        j = 1
        while j<len(A):
            u, v = P[-1]
            p, q = A[j]
            if u == q:
                P.append((p, q))
            j += 1
        P.reverse()       
        return P
     
    def _findPath(self)->tuple[bool,list[tuple[str,str]]|None]:
        """
        Find the path, where the flow can increase

        Returns
        ------
        b: return True if there is a path
        P: the path: list of edges
        """
        L:list[str] = list()
        Q: list[tuple[str|None, str]] = [(None,self._src)]
        A:list[tuple[str,str]] = list()
        while len(Q) > 0:
            s,v = Q.pop(0)
            if v == self._dst and s:
                A.append((s,v))
                return True, self._findPathSub(A)
            if v not in L:
                if s is not None:
                    A.append((s,v))
                for v, w in self._GAux.edges(v):
                    if ((v, w) not in Q) and (self._GAux.edges[v,w]['weight']>0):
                        Q.append((v,w))
                L.append(v)
        return False, None
    
    def _createAux(self) -> None:
        """
        Create Auxiliary NEtwork
        """
        self._GAux = nx.DiGraph()
        self._GAux.add_nodes_from(self._G.nodes)
        edgeList=list()
        edgeList2=dict()
        for u,v in self._G.edges:
            weight = self._G.edges[u,v]['weight']
            edgeList.append((u,v,weight))
            edgeList.append((v,u,0))
            edgeList2[(u,v)]='+' #E^{+}
            edgeList2[(v,u)]='-' #E^{-}
        self._GAux.add_weighted_edges_from(edgeList)
        nx.set_edge_attributes(self._GAux, edgeList2, 'direction')

    def _update(self,P:list[tuple[str,str]]) -> None:
        """
        Update auxiliary network
        """
        w = list()
        for u,v in P:
            weight = self._GAux.edges[u,v]['weight']
            w.append(weight)
        d = min(w)
        for u,v in P:
            self._GAux.edges[u,v]['weight'] -= d
            self._GAux.edges[v,u]['weight'] += d
        self._updatePath = P

    def _deploy(self) -> None:
        """
        Set the flow to the network from the auxiliary network
        """
        for u,v in self._GAux.edges:
            if self._GAux.edges[u,v]['direction']=='-':
                w = self._GAux.edges[u,v]['weight']
                self._G.edges[v,u]['flow']=w

    def oneStep(self)->bool:
        b,P = self._findPath()
        if b and P:
            self._update(P)
        return b
    
    def findMax(self) -> None:
        while self.oneStep():
            pass
        self._deploy()

    @property
    def G(self) -> nx.DiGraph:
        return self._G
    @property
    def GAux(self) -> nx.DiGraph:
        return self._GAux
    @property
    def updatePath(self) -> list[tuple[str, str]]:
        return self._updatePath
