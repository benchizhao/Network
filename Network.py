import networkx as nx
import logbin230119 as lb
import numpy as np
import random
import matplotlib.pyplot as plt

class BAModel:
    # The init_points is the nodes in initial graph, N is the number of nodes we add into system.
    def __init__(self,init_point,N,m):
        self.N = N
        self.m = m
        self.init_point = init_point
        self.G = nx.Graph()
        self.nodes = []
        self.edges = []
        self.degrees = []
        self.k = []
        self.t = 0


    def initial_graph(self):
        init_nodes = range(0,self.init_point)
        edd = []
        for i in range(self.init_point*(self.init_point-1)):
            x_source = list(init_nodes)
            x = random.choice(x_source)
            x_source.remove(x)
            y = random.choice(x_source)
            if x < y:
                edd.append([x,y])
        init_edges = np.unique(edd,axis = 0)

        self.G.add_nodes_from(init_nodes)
        self.G.add_edges_from(init_edges)
        self.nodes = list(self.G.nodes)
        # self.edges = self.G.edges
        self.degrees = list(np.array(self.G.degree)[:,-1])


        nx.draw_circular(self.G, with_labels=True, font_weight='bold')
        plt.show(block=True)


    def add_points(self):
        self.initial_graph()
        node = len(self.nodes)
        # print(self.degrees)
        for i in range(self.m,self.m+self.N):
            self.t += 1
            prob = self.degrees / np.sum(self.degrees)
            choose_point = np.random.choice(self.nodes, self.m, True, prob)
            self.nodes.append(node)
            self.degrees.append(self.m)
            node += 1
            for j in choose_point:
                self.degrees[j] += 1
            if self.t%1000 == 0:
                print(self.t/1000)
        # nx.draw_circular(self.G, with_labels=True)
        # plt.show(block=True)

    def add_points2(self):
        self.initial_graph()
        node = len(self.nodes)
        # print(self.degrees)
        for i in range(self.m,self.m+self.N):
            self.t += 1
            choose_point = np.random.choice(self.nodes, self.m, False)
            self.nodes.append(node)
            self.degrees.append(self.m)
            node += 1
            for j in choose_point:
                self.degrees[j] += 1
            if self.t%1000 == 0:
                print(self.t/1000)

# Model = BAModel(8,10,8)
# Model.initial_graph()