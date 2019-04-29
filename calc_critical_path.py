from hexagons import generateHexagonCenters
from hexagons import createGraph
import matplotlib.pyplot as plt
plt.rcParams.update({'font.size': 18})

def midPoint(p1, p2):
    if (not p1) or (not p2):
        return None
    x1 = p1[0]
    y1 = p1[1]
    x2 = p2[0]
    y2 = p2[1]

    return ((x1 + x2)/2, (y1 + y2)/2)


def make_set(adjList):
    parent = {}
    rank = {}

    for x in adjList.keys():
        parent[x] = x
        rank[x] = 0
    return parent, rank

def find_set(parent, rank, x):
    if parent[x] != x:
        parent[x] = find_set(parent, rank, parent[x])
    return parent[x]

def set_union(parent, rank, x, y):
    if parent[x] == parent[y]:
        return
    
    xroot = find_set(parent, rank, x)
    yroot = find_set(parent, rank, y)

    if rank[xroot] < rank[yroot]:
        tmp = xroot
        xroot = yroot
        yroot = tmp
    
    parent[yroot] = xroot

    if rank[xroot] == rank[yroot]:
        rank[xroot] += 1
    return


# Finding maximum spanning tree
def MST_kruskal(adjList, edgeWeights):
    parent, rank = make_set(adjList)

    sortedEdges = [(edge, edgeWeights[edge]) for edge in sorted(edgeWeights, key=edgeWeights.get, reverse=True)]

    mst = {}
    totalwt = 0

    for edge, weight in sortedEdges:
        x = edge[0]
        y = edge[1]

        xroot = find_set(parent, rank, x)
        yroot = find_set(parent, rank, y)

        if (xroot != yroot):
            if mst.get(x) is None:
                mst[x] = [y]
            else:
                mst[x].append(y)
            if mst.get(y) is None:
                mst[y] = [x]
            else:
                mst[y].append(x)
            set_union(parent, rank, x, y)
            totalwt += weight
    
    return mst, totalwt


if __name__ == "__main__":
    n = 3
    r = 10

    hexagons = generateHexagonCenters(n, None, r)
    hexGraph, verticesDict, adjList, pointParam, edgeWeights = createGraph(hexagons, r)

    x = []
    y = []
    points = []

    for v in verticesDict:
        # print(type(v))
        x.append(v[0])
        y.append(v[1])
        points.append((x[-1], y[-1]))
        # print(str(x[-1]) + ', ' + str(y[-1]))

    # print(adjList)

    mst, totalwt = MST_kruskal(adjList, edgeWeights)
    numC, numI, numA = 0, 0, 0

    i = 0
    for p in points:
        for adj in adjList[p]:
            # plt.plot((p[0], adj[0]), (p[1], adj[1]), 'bo-', linewidth=1)
            m = midPoint(p, adj)
            if edgeWeights.get((p, adj)) is not None:
                plt.annotate(str(edgeWeights[(p, adj)]), m)
            else:
                plt.annotate(str(edgeWeights[(adj, p)]), m)
        if len(adjList[p]) == 2:
            # print(adjList[p])
            i += 1
    for p in points:
        plt.plot(p[0], p[1], 'ro')
        plt.annotate(pointParam[p], p)
        
        for q in mst[p]:
            plt.plot((p[0], q[0]), (p[1], q[1]), 'ro-', linewidth=3.5)
            if pointParam[q] == 'C':
                numC += 1
            elif pointParam[q] == 'I':
                numI += 1
            else:
                numA += 1

    print('\nOut of ' + str(len(points)) + ' points, ' + str(i) + ' have only two adjacent points.')

    plt.show()

    print('Sum of weights of critical path = ' + str(totalwt))
    print('Total C servers: {}, I servers: {}, A servers: {}'.format(numC, numI, numA))