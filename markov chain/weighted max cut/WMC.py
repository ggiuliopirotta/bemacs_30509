from copy import deepcopy
import matplotlib.pyplot as plt
import numpy as np
from numpy import random as rnd

class Wmc:
    def __init__(self, n, prob):
        self.n = n
        self.x, self.y = rnd.random(n), rnd.random(n)

        self.m = self.config_matrix(prob)
        self.p = [[], []]

    def config_matrix(self, prob):
        n, x, y = self.n, self.x, self.y

        mat = np.zeros((n, n))
        for i in range(n):
            for j in range(i+1, n):
                if rnd.random() < prob:
                    mat[i, j] = np.sqrt((x[i]-x[j])**2 + (y[i]-y[j])**2)
                    mat[j, i] = mat[i, j]

        return mat
    
    def init_config(self):
        n = self.n

        part1 = np.sort(rnd.choice(np.arange(n), rnd.randint(1, n-1), replace=False))
        part2 = np.delete(np.arange(n), part1)

        self.p[0], self.p[1] = part1, part2
    
    def propose_move(self):
        p = self.p

        p_choice = rnd.randint(2)
        if len(p[p_choice]) <= 1:
            p_choice = 1-p_choice

        p_from = p[p_choice]
        v_ind = rnd.choice(len(p_from))
        v = p_from[v_ind]

        return v_ind, v, p_choice

    def accept_move(self, move):
        p = self.p
        v_ind, v, p_choice = move

        p_from, p_to = p[p_choice], p[1-p_choice]
        p_from, p_to = np.delete(p_from, v_ind), np.sort(np.append(p_to, v))
        p[p_choice], p[1-p_choice] = p_from, p_to

        return self
    
    def compute_delta_cost(self, move):
        m, p = self.m, self.p
        v, p_choice = move[1], move[2]

        w_old = np.sum(m[v, p[1-p_choice]])
        w_new = np.sum(m[v, p[p_choice]])

        w_delta = w_new-w_old
        return w_delta

    def compute_cost(self):
        n, m, p = self.n, self.m, self.p

        w = 0.0
        for i in range(n):
            for j in range(i+1, n):
                if (i in p[0] and j in p[1]) or (i in p[1] and j in p[0]):
                    w += m[i, j]

        return w

    def display(self):
        n, x, y, m, p = self.n, self.x, self.y, self.m, self.p

        plt.pause(0.01)
        plt.figure(1)
        plt.clf()

        for i in range(n):
            for j in range(i+1, n):
                if m[i, j] != 0:
                    xx = [x[i], x[j]]
                    yy = [y[i], y[j]]

                    if (i in p[0] and j in p[1]) or (i in p[1] and j in p[0]):
                        plt.plot(xx, yy, color='green', alpha=0.5)

                    else:
                        plt.plot(xx, yy, color='grey', alpha=0.3)

        plt.plot(x[p[0]], y[p[0]], 'ro')
        plt.plot(x[p[1]], y[p[1]], 'bo')
    
    def copy(self):
        return deepcopy(self)
