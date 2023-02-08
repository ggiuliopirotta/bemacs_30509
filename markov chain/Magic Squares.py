from Greedy import greedy
from Simulation Annealing import sim_ann

from copy import deepcopy
from numpy import random as rnd
import numpy as np

class Magic_Squares:
    def __init__(self, n, s, seed=None):
        if seed is not None:
            rnd.seed(seed)

        self.n = n
        self.s = s
        self.table = np.zeros((n, n))

    def __str__(self):
        return str(self.table)

    def init_config(self):
        n, s = self.n, self.s

        for i in range(n):
            self.table.T[i] = rnd.randint(1, s-n+2, size=n)

    def propose_move(self):
        n, table = self.n, self.table

        i, j = rnd.randint(n, size=2)
        num = rnd.choice([max(table[i, j]-1, 1), table[i, j]+1])

        return i, j, num

    def accept_move(self, move):
        i, j, num = move

        self.table[i, j] = num

    def compute_delta_cost(self, move):
        n, s, table = self.n, self.s, self.table
        i, j, num = move

        row_old, col_old = table[i], table.T[j]
        row_new, col_new = row_old.copy(), col_old.copy()
        row_new[j], col_new[i] = num, num

        c_delta = check_error(row_new, s) + check_error(col_new, s)
        c_delta -= check_error(row_old, s) + check_error(col_old, s)

        if i == j:
            diag1_old = get_diag(table, n)[0]
            diag1_new = diag1_old.copy()
            diag1_new[j] = num

            c_delta += check_error(diag1_new, s)-check_error(diag1_old, s)

        if j == n-1-i:
            diag2_old = get_diag(table, n)[1]
            diag2_new = diag2_old.copy()
            diag2_new[i] = num

            c_delta += check_error(diag2_new, s)-check_error(diag2_old, s)

        return c_delta

    def compute_cost(self):
        n, s, table = self.n, self.s, self.table

        c = 0
        for i in range(n):
            c += check_error(table[i], s)
            c += check_error(table.T[i], s)

        diag1, diag2 = get_diag(table, n)
        c += check_error(diag1, s) + check_error(diag2, s)
        return c

    def copy(self):
        return deepcopy(self)

    def display(self):
        print(self)

def get_diag(matrix,  n):
    diag1, diag2 = np.zeros(n), np.zeros(n)

    for i in range(n):
        diag1[i], diag2[i] = matrix[i, i], matrix[i, n-1-i]

    return diag1, diag2

def check_error(array, s):
    err = abs(np.sum(array)-s)
    return err

magic_sq = Magic_Squares(n=6, s=250)
greedy(magic_sq, iters=50000, restarts=2)
