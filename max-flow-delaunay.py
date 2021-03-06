import sys
from collections import namedtuple
from itertools import permutations, combinations
from flow import FlowNetwork
import delaunay
import math

Point = namedtuple('Point', 'x y index')

Infinity = float("inf")

def slope(a, b):
    return (b.y - a.y) / (b.x - a.x) if b.x - a.x != 0 else Infinity

def dist(a, b):
    return math.sqrt((b.y - a.y)**2 + (b.x - a.x)**2)

def farthest_points(points):
    return max(permutations(points, 2), key=lambda (a, b): (dist(a, b), slope(a, b)))

def dot_edge(edge, flow, maxflow):
    label = "%5.3f/%5.3f" % (flow, edge.c)
    weight = 1 + 9 * float(flow)/maxflow
    opacity = 220 - int(flow/edge.c * 220)
    color = "#%02x%02x%02x" % ((opacity,) * 3)
    a, b = edge.a.index, edge.b.index
    return '%d -- %d [label="%s", penwidth="%f", color="%s"]\n' % (a, b, label, weight, color)

def dot_point(point, shape="circle"):
    return '%d [pos="%f,%f!",shape="%s"]\n' % (point.index, point.x, point.y, shape)

def dot_output(network, maxflow, s, t, filename='out.dot'):
    #prints the flow network to a file in dot format
    points = network.vertices()
    with open('out.dot', 'w') as f:
        f.write('graph maxflow {\n')
        for point in points:
            f.write(dot_point(point))
        for point in [s, t]:
            f.write(dot_point(point, "doublecircle"))
        edges = (edge for edge in network.edges() if edge.a.index < edge.b.index)
        for edge in edges:
            f.write(dot_edge(edge, abs(network.flow[edge]), maxflow))
        f.write('}\n')

def console_output(network, maxflow, s, t):
    #print the source and sink
    for v in [s,t]: print "%d\t(%d, %d)" % (v.index, v.x, v.y)

    #print the max flow
    print "%.5f" % maxflow

    #print the edges in lexicographic order along with capacity and flow info
    edges = [edge for edge in network.edges() if edge.a.index < edge.b.index]
    for edge in sorted(edges, key=lambda e: [e.a.index, e.b.index]):
        print "%d\t%d\t%10.5f\t%10.5f" % (edge.a.index, edge.b.index, edge.c, abs(network.flow[edge]))

def main():
    #reading from file
    with open(sys.argv[1], 'r') as f:
        n = int(f.readline())
        points = [Point._make(map(float, line.split()) + [i+1]) for i, line in enumerate(f)]

    #sort by (x, y)
    points = sorted(points)

    delaunay_edges = delaunay.from_points(points)

    network = FlowNetwork(points)
    for u, v in delaunay_edges:
        network.add_edge(u, v, dist(u, v))

    s, t = farthest_points(points)
    flow = network.max_flow(s, t)

    console_output(network, flow, s, t)
    dot_output(network, flow, s, t)

if __name__ == '__main__':
    main()
