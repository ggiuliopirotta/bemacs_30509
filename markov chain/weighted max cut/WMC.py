from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from numpy import random as rnd

class Wmc:
    def __init__(self, n, p, seed=None):
        if seed is not None:
            np.random.seed(seed)

        self.n = n
        self.x, self.y = rnd.random(n), rnd.random(n)

        self.partition = [[], []]
        self.graph = self.config_graph(p)

    def config_graph(self, p):
        n, x, y = self.n, self.x, self.y

        graph = np.zeros((n, n))
        for i in range(n):
            for j in range(i+1, n):
                if rnd.random() < prob:
                    graph[i, j] = np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2)
                    graph[j, i] = graph[i, j]

        return graph
    
    def init_config(self):
        n = self.n

        part1 = np.sort(rnd.choice(np.arange(n), rnd.randint(1, n-1), replace=False))
        part2 = np.delete(np.arange(n), part1)

        self.partition[0], self.partition[1] = part1, part2
    
    def propose_move(self):
        partition = self.partition

        p_choice = rnd.randint(2)
        if len(partition[p_choice]) <= 1:
            p_choice = 1-p_choice

        p_from = partition[p_choice]
        v_ind = rnd.choice(len(p_from))
        v = p_from[v_ind]

        return v_ind, v, p_choice

    def accept_move(self, move):
        partition = self.partition
        v_ind, v, p_choice = move

        p_from, p_to = partition[p_choice], partition[1-p_choice]
        p_from, p_to = np.delete(p_from, v_ind), np.sort(np.append(p_to, v))
        self.partition[p_choice], self.partition[1-p_choice] = p_from, p_to
    
    def compute_delta_cost(self, move):
        partition, graph = self.partition, self.graph
        v, p_choice = move[1], move[2]

        w_old = np.sum(graph[v, partition[1-p_choice]])
        w_new = np.sum(graph[v, partition[p_choice]])

        w_delta = w_new-w_old
        return w_delta

    def compute_cost(self):
        n, partition, graph = self.n, self.partition, self.graph

        w = 0.0
        for i in range(n):
            for j in range(i+1, n):
                if (i in partition[0] and j in partition[1]) or (i in partition[1] and j in partition[0]):
                    w += graph[i, j]

        return w

    def display(self):
        n, x, y, partition, graph = self.n, self.x, self.y, self.partition, self.graph

        plt.pause(0.01)
        plt.figure(1)
        plt.clf()

        for i in range(n):
            for j in range(i+1, n):
                if graph[i, j] != 0:
                    xx = [x[i], x[j]]
                    yy = [y[i], y[j]]

                    if (i in partition[0] and j in partition[1]) or (i in partition[1] and j in partition[0]):
                        plt.plot(xx, yy, color='green', alpha=0.5)

                    else:
                        plt.plot(xx, yy, color='grey', alpha=0.3)

        plt.plot(x[p[0]], y[p[0]], 'ro')
        plt.plot(x[p[1]], y[p[1]], 'bo')
    
    def copy(self):
        return deepcopy(self)
