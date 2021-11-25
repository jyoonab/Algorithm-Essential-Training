class Graph:
    def __init__(self, num_edge, vertices):
        self.vertex = [[]]
        self.num_edge = num_edge
        for num in range(num_edge):
            self.vertex.append([])
        self.createGraph(vertices)

    def createGraph(self, vertices):
        for vertex in vertices:
            self.vertex[vertex[0]].append(vertex[1])
            self.vertex[vertex[1]].append(vertex[0])
        print(self.vertex)

    def getFarestNodes(self):
        dist = []
        counter = 0
        time = len(self.vertex)

        for i in range(len(self.vertex)):
            if i == 1 or i == 0:
                dist.append(-1)
            else:
                dist.append(0)

        while time > 0:
            time -= 1
        return 0

class DataStructure:
    def stack(list, n):
        list = list
        list.append(n)
        return list
    def deStack(list):
        return list[:-1]
    def deQueue(list):
        return list[1:]


def solution(n, edge):
    g = Graph(n, edge)
    return g.getFarestNodes()

input1 = 6
input2 = [[3, 6], [4, 3], [3, 2], [1, 3], [1, 2], [2, 4], [5, 2]]

solution(input1, input2)
