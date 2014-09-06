import math
from collections import namedtuple, deque

Edge = namedtuple('Edge', 'a b c')

def dist(a, b):
    return math.sqrt((a.x - b.x)**2 + (a.y - b.y)**2)

class FlowNetwork(object):
    def __init__(self, vertices = [], edges = []):
        self._adj = {}
        self.flow = {}
        self._redge = {}
        for v in vertices: self.add_vertex(v)
        for e in edges: self.add_edge(e)

    def vertices(self):
        return self._adj.keys()

    def edges(self):
        return self.flow.keys()

    def add_vertex(self, v):
        self._adj[v] = []

    def add_edge(self, a, b, c):
        assert a != b
        edge = Edge(a, b, c)
        redge = Edge(b, a, c)
        self._redge[edge] = redge
        self._redge[redge] = edge
        self._adj[a].append(edge)
        self._adj[b].append(redge)
        self.flow[edge] = 0
        self.flow[redge] = 0

    def max_flow(self, s, t):
        #import pdb; pdb.set_trace()
        path = self.__bfs(s,t)
        while len(path) > 0:
            flow = min([e.c - self.flow[e] for e in path])
            for e in path:
                self.flow[e] += flow
                self.flow[self._redge[e]] -= flow
            path = self.__bfs(s, t)
        return sum([self.flow[edge] for edge in self._adj[s]])

    def __bfs(self, s, t):
        q = deque([s])
        pred = {}
        while len(q) > 0:
            vertex = q.popleft()
            if vertex == t:
                path = []
                while vertex != s:
                    path.append(pred[vertex])
                    vertex = pred[vertex].a
                return list(reversed(path))
            es = [e for e in self._adj[vertex] if e.c - self.flow[e] > 0 and not (e.b in pred)]
            for e in es:
                pred[e.b] = e
                q.append(e.b)
        return []
