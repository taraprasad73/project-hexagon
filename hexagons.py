import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import argparse
import math


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
def generateHexagons(numLayers, numHexagons, radius):
    hexagons = []
    hexagonCountReached = False
    for layer in range(numLayers):
        r = layer * math.sqrt(3) * radius
        if layer == 0:
            hexagon = Hexagon(Corner(0, 0))
            hexagons.append(hexagon)
        else:
            delta = 360 / (layer * 6)
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


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Input for the hexagons")
    parser.add_argument("n", type=int, help="total number of layers")
    parser.add_argument("r", type=int, help="radius of hexagon")
    parser.add_argument("-c", type=int, help="total count of hexagons")
    args = parser.parse_args()

    numLayers = args.n
    numHexagons = args.c
    radius = args.r

    hexagons = generateHexagons(numLayers, numHexagons, radius)

    verticesDict = {}
    hexGraph = nx.Graph()
    for hexagon in hexagons:
        center = hexagon.center
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

        hexagon.addPoints(points)

    pos = nx.get_node_attributes(hexGraph, 'pos')
    nx.draw(hexGraph, pos=pos, node_size=1)
    plt.savefig('hex.png', dpi=600)
