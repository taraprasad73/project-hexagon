import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import math
import os
import random

if not os.path.exists('data'):
    os.makedirs('data')

HEXAGON_IMAGE_FILE_PATH = 'data/hex.png'


class Corner:
    def __init__(self, x, y):
        self.position = (x, y)
        self.x = x
        self.y = y


class Hexagon:
    def __init__(self, center):
        self.center = center

    def addPoints(self, points):
        self.points = points


# Works till layer = 3
def generateHexagonCenters(numLayers, numHexagons, radius):
    hexagons = []
    hexagonCountReached = False
    for layer in range(numLayers):
        r = layer * math.sqrt(3) * radius
        if layer == 0:
            hexagon = Hexagon(Corner(0, 0))
            hexagons.append(hexagon)
        else:
            delta = 360 // (layer * 6)
            for theta in range(0, 360, delta):
                if layer == 2 and (theta - 30) % 60 == 0:
                    x = 3 * radius * math.cos(math.radians(theta))
                    y = 3 * radius * math.sin(math.radians(theta))
                else:
                    x = r * math.cos(math.radians(theta))
                    y = r * math.sin(math.radians(theta))
                hexagon = Hexagon(Corner(x, y))
                hexagons.append(hexagon)
                if numHexagons is not None and len(hexagons) >= numHexagons:
                    hexagonCountReached = True
                    break
            if hexagonCountReached:
                break
    return hexagons


def createGraph(hexagons, radius):
    hexGraph = nx.Graph()
    verticesDict = {}
    adjList = {}
    pointParam = {}   # Each point has a certain param, C or I or A
    params = ['C', 'I', 'A']    # Confidentiality, Integrity and Authenticity
    edgeWeights = {}    # key is tuple of pair of point tuples

    for hexagon in hexagons:
        center = hexagon.center
        hexWeight = random.randint(1, 5)
        points = []
        for theta in range(30, 360, 60):
            x = round(center.x + radius * math.cos(math.radians(theta)), 2)
            y = round(center.y + radius * math.sin(math.radians(theta)), 2)

            position = (x, y)
            if verticesDict.get(position) is None:
                point = Corner(x, y)
                verticesDict[position] = point
                hexGraph.add_node(point, pos=point.position)
            else:
                point = verticesDict[position]
            points.append(point)

        for i in range(6):
            hexGraph.add_edge(points[(i + 1) % 6], points[i])
            positionA = (points[i].x, points[i].y)
            positionB = (points[(i + 1)%6].x, points[(i + 1)%6].y)
            
            if edgeWeights.get((positionA, positionB)) is None:
                if edgeWeights.get((positionB, positionA)) is None:
                    edgeWeights[(positionA, positionB)] = hexWeight
                else:
                    edgeWeights[(positionB, positionA)] += hexWeight
            else:
                edgeWeights[(positionA, positionB)] += hexWeight

            if adjList.get(positionA) is None:
                adjList[positionA] = [(positionB)]
            elif positionB not in adjList[positionA]:
                adjList[positionA].append(positionB)

            if adjList.get(positionB) is None:
                adjList[positionB] = [positionA]
            elif positionA not in adjList[positionB]:
                adjList[positionB].append(positionA)
            
        i = 0
        for p in points:
            p = (p.x, p.y)
            if pointParam.get(p) is None:
                pointParam[p] = params[i]
                i += 1
                i %= 3

        hexagon.addPoints(points)
    return hexGraph, verticesDict, adjList, pointParam, edgeWeights


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input for the hexagons")
    parser.add_argument("n", type=int, help="total number of layers")
    parser.add_argument("r", type=int, help="radius of hexagon")
    parser.add_argument("-c", type=int, help="total count of hexagons")
    args = parser.parse_args()

    numLayers = args.n
    numHexagons = args.c
    radius = args.r

    hexagons = generateHexagonCenters(numLayers, numHexagons, radius)
    hexGraph, verticesDict, *rest = createGraph(hexagons, radius)

    pos = nx.get_node_attributes(hexGraph, 'pos')
    nx.draw(hexGraph, pos=pos, node_size=1)
    plt.savefig(HEXAGON_IMAGE_FILE_PATH, dpi=600)
