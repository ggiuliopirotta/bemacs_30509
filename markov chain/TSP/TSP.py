from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from numpy import random as rnd

class Tsp:
    def __init__(self, n, seed=None):
        if seed is not None:
            rnd.seed(seed)

        self.n = n
        self.x, self.y = rnd.random(n), rnd.random(n)
        self.dist = np.zeros((n, n))

        for e1 in range(n):
            for e2 in range(e1+1, n):
                self.dist[e1, e2] = self.compute_dist(e1, e2)
                self.dist[e2, e1] = self.dist[e1, e2]

        self.route = np.arange(n)

    def init_config(self):
        n = self.n

        self.route[:] = rnd.permutation(n)
    
    def couple_edges(self):
        n = self.n

        e_pairs = []
        for e1 in range(n):
            for e2 in range(n):
                if e1 < e2 and (e1-1)%n != e2 and (e1+1)%n != e2:
                    e_pairs.append((e1, e2))

        return e_pairs

    def propose_move(self):
        n = self.n

        while True:
            e1 = rnd.randint(n)
            e2 = rnd.randint(n)

            if e2 < e1:
                e1, e2 = e2, e1

            if e1 != e2 and (e1-1)%n != e2 and (e1+1)%n != e2:
                break

        return e1, e2
        
    def accept_move(self, move):
        e1, e2 = move

        self.route[e1+1:e2+1] = self.route[e2:e1:-1]
    
    def compute_dist(self, e1, e2):
        x, y = self.x, self.y

        dist = np.sqrt((x[e1]-x[e2])**2 + (y[e1]-y[e2])**2)
        return dist

    def compute_delta_cost(self, move):
        n, dist, route = self.n, self.dist, self.route
        e1, e2 = move

        e1_prev, e1_next = route[e1], route[(e1+1)%n]
        e2_prev, e2_next = route[e2], route[(e2+1)%n]

        c_old = dist[e1_prev, e1_next] + dist[e2_prev, e2_next]
        c_new = dist[e1_prev, e2_prev] + dist[e1_next, e2_next]

        c_delta = c_new-c_old
        return c_delta

    def compute_cost(self):
        n, dist, route = self.n, self.dist, self.route

        c = 0.0
        for e in range(n):
            c += dist[route[e], route[(e+1)%n]]
        return c

    def display(self):
        x, y, route = self.x, self.y, self.route

        plt.pause(0.01)
        plt.figure(1)
        plt.clf()

        plt.plot(x[route], y[route], color='orange')

        e_last = [route[-1], route[0]]
        plt.plot(x[e_last], y[e_last], color='orange')

        plt.plot(x, y, 'o', color='blue')

    def copy(self):
        return deepcopy(self)
