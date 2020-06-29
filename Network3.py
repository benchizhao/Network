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
        self.node = len(self.nodes)
        self.degrees = list(np.array(self.G.degree)[:,-1])



    def add_node(self,q):
        self.initial_graph()
        for k in range(self.m,self. m+self.N):
            self.degrees.append(0)
            p = np.random.random()
            for i in range(self.m):
                if p < 1-q:
                    prob = self.degrees[:-1] / np.sum(self.degrees[:-1])
                    choose_point = np.random.choice(self.nodes, 1, False, prob)[0]
                    self.degrees[choose_point] += 1
                    self.degrees[-1] += 1
                else:
                    choose_point = np.random.choice(self.nodes)
                    self.degrees[choose_point] += 1
                    self.degrees[-1] += 1
            self.nodes.append(self.node)
            self.node += 1
    #         if self.t % 1000 == 0:
    #             print(self.t / 1000)


# model = BAModel(6,10,3)
# model.add_node(0.5)
#
#
# print(len(model.degrees))
# print(model.degrees)
# print(len(model.nodes))
# print(model.nodes)