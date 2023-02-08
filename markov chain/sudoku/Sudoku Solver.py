from copy import deepcopy
import numpy as np
from numpy import random as rnd

class Sdk_Solver:
    def __init__(self, obj):
        self.n = obj.n
        self.sn = int(np.sqrt(obj.n))

        self.table = obj.table
        self.mask = obj.mask
    
    def __repr__(self):
        return str(self.table)
    
    def __add__(self, num):
        return self.table+num
    
    def init_config(self):
        n, table, mask = self.n, self.table, self.mask

        for i in range(n):
            col = table.T[i]
            mask_fix = mask.T[i]

            l = np.arange(n)
            l = np.delete(l, col[mask_fix])

            col[(mask_fix == False)] = rnd.permutation(l)
    
    def propose_move(self):
        n, mask = self.n, self.mask

        i = rnd.randint(n)
        mask_col = mask.T[i]
        ind_free = np.where(mask_col == False)[0]

        moves = np.arange(n)
        j, k = rnd.choice(moves[ind_free], 2, replace=False)
        return i, j, k
    
    def accept_move(self, move):
        i, j, k = move

        self.table[j, i], self.table[k, i] = self.table[k, i], self.table[j, i]
 
    def compute_delta_cost(self, move):
        c_old = self.compute_cost()
        table_new = self.copy()
        table_new.accept_move(move)
        c_new = table_new.compute_cost()

        c_delta = c_new-c_old
        return c_delta

    def compute_cost(self):
        n, sn, table = self.n, self.sn, self.table

        c = 0
        for i in range (n):
            c += check_error(table[i])
            c += check_error(table.T[i])

        for si in range(sn):
            for sj in range(sn):
                table_ij = table[si*sn:(si+1)*sn, sj*sn:(sj+1)*sn]
                c += check_error(table_ij)

        return c

    def display(self):
        n, sn, table = self.n, self.sn, self.table

        grid = table.copy()+1
        sdk = str()
        for i in range(n):
            sdk += '| '

            for j in range(sn):
                sub = grid[i, j*sn:(j+1)*sn]

                for k in sub:
                    sdk += f'{k} '

                sdk += '| '

            if i in [h*sn-1 for h in range (1, sn)]:
                sdk += '\n-------------------------\n'

            else:
                sdk += '\n'

        print (sdk)
    
    def copy (self):
        return deepcopy (self)

def check_error(array):
    if array.size == 0:
        err = 0
    else:
        err = array.size-np.unique(array).size

    return err
