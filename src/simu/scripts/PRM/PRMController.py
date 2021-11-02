from collections import defaultdict
import sys
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import Rectangle
import numpy as np
from sklearn.neighbors import NearestNeighbors
import shapely.geometry
import argparse

from Dijkstra import Graph, dijkstra, to_array
from Utils import Utils


class PRMController:
    def __init__(self, numOfRandomCoordinates, allObs, current, destination, large, high):
        self.numOfCoords = numOfRandomCoordinates
        self.coordsList = np.array([])
        self.allObs = allObs
        self.current = np.array(current)
        self.destination = np.array(destination)
        self.graph = Graph()
        self.utils = Utils()
        self.solutionFound = False
        self.large = large
        self.high = high

    def runPRM(self, saveImage=True):

        # Fica no looping ate achar uma solucao
        while(not self.solutionFound):

            seed = np.random.randint(1, 100000)
            # print("Trying with random seed {}".format(seed)) #escolhe uma seed aleatoria 
            np.random.seed(seed)

            # Gera os n pontos no mapa
            self.genCoords()

            # verificando se o houve colisao com obstaculo
            self.checkIfCollisonFree()

            # achar os k vizinhos mais proximos
            # verificar se as ligacoes entre os pontos colidem com obstaculos
            self.findNearestNeighbour()

            # encontrando menor caminho usando dijkstra
            self.shortestPath()

            
        self.coordsList = np.array([])
        self.graph = Graph()

        if(saveImage):
            plt.savefig("../../mapa/{}_samples.png".format(self.numOfCoords))

        #Ajustando a escala para metros
        locsx, lables = plt.xticks()
        locsy, lables = plt.yticks()

        my_xticks = ['-2','1','0','1','2','3','4','5','6','7','8','9','10']
        my_yticks = ['-1','0','1','2','3','4','5','6','7','8']
        plt.xticks(np.arange(locsx.min(),locsx.max(), 50), my_xticks)
        plt.yticks(locsy, my_yticks)

        plt.xlim(0, self.large)
        plt.ylim(0, self.high)
        plt.show()

    def genCoords(self, maxSizeOfMap=100):
        xs = np.random.randint(self.large, size=(self.numOfCoords, 1))
        ys = np.random.randint(self.high, size=(self.numOfCoords, 1))

        self.coordsList = np.hstack((xs, ys))

        # Adding begin and end points
        self.current = self.current.reshape(1, 2)
        self.destination = self.destination.reshape(1, 2)
        self.coordsList = np.concatenate(
            (self.coordsList, self.current, self.destination), axis=0)

    def checkIfCollisonFree(self):
        collision = False
        self.collisionFreePoints = np.array([])
        for point in self.coordsList:
            collision = self.checkPointCollision(point)
            if(not collision):
                if(self.collisionFreePoints.size == 0):
                    self.collisionFreePoints = point
                else:
                    self.collisionFreePoints = np.vstack(
                        [self.collisionFreePoints, point])
        self.plotPoints(self.collisionFreePoints)

    def findNearestNeighbour(self, k=10):
        X = self.collisionFreePoints
        knn = NearestNeighbors(n_neighbors=k)
        knn.fit(X)
        distances, indices = knn.kneighbors(X)
        self.collisionFreePaths = np.empty((1, 2), int)

        for i, p in enumerate(X):
            # Ignoring nearest neighbour - nearest neighbour is the point itself
            for j, neighbour in enumerate(X[indices[i][1:]]):
                start_line = p
                end_line = neighbour
                if(not self.checkPointCollision(start_line) and not self.checkPointCollision(end_line)):
                    if(not self.checkLineCollision(start_line, end_line)):
                        self.collisionFreePaths = np.concatenate(
                            (self.collisionFreePaths, p.reshape(1, 2), neighbour.reshape(1, 2)), axis=0)

                        a = str(self.findNodeIndex(p))
                        b = str(self.findNodeIndex(neighbour))
                        self.graph.add_node(a)
                        self.graph.add_edge(a, b, distances[i, j+1])
                        x = [p[0], neighbour[0]]
                        y = [p[1], neighbour[1]]
                        plt.plot(x, y)

    def shortestPath(self):
        self.startNode = str(self.findNodeIndex(self.current))
        self.endNode = str(self.findNodeIndex(self.destination))

        dist, prev = dijkstra(self.graph, self.startNode)

        pathToEnd = to_array(prev, self.endNode)

        if(len(pathToEnd) > 1):
            self.solutionFound = True
        else:
            return

        # Plotting shorest path
        pointsToDisplay = [(self.findPointsFromNode(path))
                           for path in pathToEnd]

        x = [int(item[0]) for item in pointsToDisplay]
        y = [int(item[1]) for item in pointsToDisplay]

        # print("DADOS DA ROTA: \n\n", x, y)

        with open('../../mapa/route.txt', 'w') as route:
            for i in range (0, len(x)):
                if(i==0):
                   route.write(str(len(x)) + "\n") 
                route.write(str(x[i]) +' ' + str(y[i]) + "\n")

        plt.plot(x, y, c="blue", linewidth=3.5)

        pointsToEnd = [str(self.findPointsFromNode(path))
                       for path in pathToEnd]
        # print("****Output****")

        # print("The quickest path from {} to {} is: \n {} \n with a distance of {}".format(
        #     self.collisionFreePoints[int(self.startNode)],
        #     self.collisionFreePoints[int(self.endNode)],
        #     " \n ".join(pointsToEnd),
        #     str(dist[self.endNode])
        # )
        # )

    def checkLineCollision(self, start_line, end_line):
        collision = False
        line = shapely.geometry.LineString([start_line, end_line])
        for obs in self.allObs:
            if(self.utils.isWall(obs)):
                uniqueCords = np.unique(obs.allCords, axis=0)
                wall = shapely.geometry.LineString(
                    uniqueCords)
                if(line.intersection(wall)):
                    collision = True
            else:
                obstacleShape = shapely.geometry.Polygon(
                    obs.allCords)
                collision = line.intersects(obstacleShape)
            if(collision):
                return True
        return False

    def findNodeIndex(self, p):
        return np.where((self.collisionFreePoints == p).all(axis=1))[0][0]

    def findPointsFromNode(self, n):
        return self.collisionFreePoints[int(n)]

    def plotPoints(self, points):
        x = [item[0] for item in points]
        y = [item[1] for item in points]
        plt.scatter(x, y, c="black", s=1)

    def checkCollision(self, obs, point):
        p_x = point[0]
        p_y = point[1]
        if(obs.bottomLeft[0] <= p_x <= obs.bottomRight[0] and obs.bottomLeft[1] <= p_y <= obs.topLeft[1]):
            return True
        else:
            return False

    def checkPointCollision(self, point):
        for obs in self.allObs:
            collision = self.checkCollision(obs, point)
            if(collision):
                return True
        return False
