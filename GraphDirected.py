from queue import Queue


class GraphDirected:
    '''
        Class;
        (*) Scope: Manage a directed graph.
    '''

    def __init__(self, filename):
        '''
            Constructor for the Graph.
            (*) param: -filename: it is the name file name where the graph is stored.
            (*) Lists: - vertices: it contains numbers, each of them representing a vertex
            (*) Dictionaries: - dictIn: it contains all the inbound vertices
                              - dictOut: it contains all the outbound vertices
                              - Costs: it contains the cost for each edge
        '''

        self._dictIn = {}
        self._dictOut = {}
        self._costs = {}
        self._vertices = []
        self.__noOfVertices = 0

        self.readFromFile(filename)

    def noOfVertices(self):
        '''
             Getter for the number of vertices in the current graph.
             Return: the number of vertices.
        '''
        return self.__noOfVertices

    def isVertex(self, x):
        '''
            It checks if  there is a given vertex in the graph.
            (*) param:  -x: the given vertex
            Return: > True if the vertex x exists
                    > False if the vertex x doesn't exist
        '''
        if x in self._vertices:
            return True
        return False

    def isEdge(self, x, y):
        '''
            It checks if there is an edge between two given vertices.
            (*) param:  -x: the inbound vertex
                        -y: the outbound vertex
            Return: > True if there is an edge between x and y
                    > False is the is no edge between x and y
        '''
        if y in self._dictOut[x]:
            return True
        return False

    def parseNout(self, x):
        '''
            It gives the list of vertices to which there exists an edge from a given vertex
            (*) param:  -x: the vertex
            Return: the list with the required vertices
        '''
        return self._dictOut[x]

    def parseNin(self, x):
        '''
            Returns the list of vertices from which there is an edge to the current vertex
            (*)param: x- The current vertex
            Return: The list
        '''
        return self._dictIn[x]

    def getCost(self, x, y):
        '''
            I gives the cost of the edge.
            (*) param -x: the inbound vertex
                      -y: the outbound vertex
            Return the cost of the edge.
        '''
        return self._costs[(x, y)]

    def setCostOfEdge(self, x, y, newCost):
        '''
            It sets the cost of an edge between two vertices to a new given value.
            (*) param -x: the inbound vertex
                      -y: the outbound vertex
                      -newCost: the new cost of the edge
        '''
        if self._costs[(x, y)] == 0:
            return
        self._costs[(x, y)] = newCost

    def addVertex(self, vertex):
        '''
            It adds a vertex to the graph by its value.
            (*) param -vertex: the vertex that will be  added to the graph
             Return: > True: if the vertex was successfully added.
                    > False: if the vertex couldn't be added.
        '''
        if vertex not in self._vertices:
            self._vertices.append(vertex)
            self._dictIn[vertex] = []
            self._dictOut[vertex] = []
            self.__noOfVertices += 1
            return True
        return False


    def addEdge(self, x, y, cost):
        '''
            It adds an edge to the graph.
            (*) param -x: the inbound vertex
                      -y: the outbound vertex
                      -cost: the cost of the new edge
             Return: > 1: if the edge was successfully added.
                    > 0: if the edge couldn't be added.

        '''
        if self.__noOfVertices == 0:
            return
        if x in self._dictOut[x]:
            return 0
        else:
            self._dictOut[x].append(y)
            self._costs[(x, y)] = cost
        if y in self._dictIn[y]:
            return 0
        else:
            self._dictIn[y].append(x)


    def readFromFile(self, fName):
        '''
            It reads a graph from a file.
            (*)param: -fName: the name of the file where the graph is sotred.
        '''
        f = open(fName, "r")
        line = f.readline().strip().split()
        n = int(line[0])
        for i in range(n):
            self.addVertex(i)
        m = int(line[1])
        line = f.readline().strip()
        for i in range(m):
            arrgs = line.split(" ")
            self.addEdge(int(arrgs[0]), int(arrgs[1]), int(arrgs[2]))
            line = f.readline().strip()
        f.close()

    def topoSort(self):

        listSorted = []
        q = Queue()
        count = {}
        for x in self._vertices:
            #nr of vertices from  where is an edge to the current edge
            count[x] = len(self.parseNin(x))
            if count[x] == 0:
                q.put(x)
        while not q.empty():
            x = q.get()
            listSorted.append(x)
            for y in self._dictOut[x]:
                count[y] = count[y] - 1
                if count[y] == 0:
                    q.put(y)
        if len(listSorted) < len(self._vertices):
            listSorted = []
        return listSorted

    def maxCostPathInDAG(self, s, t):
        topoSorted = self.topoSort()
        costs = {}
        # get all costs from the graph
        for v in self._costs.keys():
            costs[v] = -self._costs[v]
        # print topoSorted
        # if topoSorted is none, the graph is not a DAG
        if topoSorted is None:
            return None
        dist = {s: 0}
        prev = {s: None}
        for x in topoSorted:
            if x in dist:
                for y in self.parseNout(x):
                    if y not in dist or dist[x] + costs[(x, y)] < dist[y]:
                        prev[y] = x
                        dist[y] = dist[x] + costs[(x, y)]
        # print dist
        if t not in dist:
            return None
        x = t
        path = []
        while x is not None:
            path.append(x)
            x = prev[x]

        path.reverse()
        return path

if __name__ == '__main__':

    g = GraphDirected("graph5.txt")
    res = g.topoSort()
    if len(res) == 0:
        print("The graph is not a DAG!\n")
    else:
        print("The graph is a DAG\n")
        v1 = int(input("Give the starting vertex : "))
        v2 = int(input("Give the ending vertex: "))
        maxCostPath = g.maxCostPathInDAG(v1, v2)
        if maxCostPath is None:
            print("There is no path between " + str(v1) + " and " + str(v2) + "\n")
        else:
            print("The highest cost path is: " + str(g.maxCostPathInDAG(v1, v2)))