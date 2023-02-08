from copy import deepcopy
import numpy as np

class Sdk_Generator:
    def __init__(self, n, r):
        self.n = n
        self.sn = int(np.sqrt(n))
        self.r = r

        self.mask = self.config_mask()
        self.table = np.ones((n, n), dtype=int)*(-1)
        self.config_table()
    
    def __repr__(self):
        return str(self.table)
    
    def __add__(self, num):
        return self.table+num

    def config_mask(self):
        n, r = self.n, self.r

        mask = np.zeros((n, n), dtype=bool)
        for i in range(n):
            for j in range(n):
                mask[i, j] = np.random.choice((0, 1), p=(1-r, r))

        return mask

    def config_table(self):
        n, mask, table = self.n, self.mask, self.table

        c = np.inf
        while c != 0:
            table[mask] = np.random.choice(np.arange(n), table[mask].size, replace=True)
            c = self.compute_cost()

    def compute_cost(self):
        n, sn, mask, table = self.n, self.sn, self.mask, self.table

        c = 0
        for i in range(n):
            c += check_error(table[i][mask[i]])
            mask_ti = mask.T[i]
            c += check_error(table.T[i][mask_ti])

        for si in range(sn):
            for sj in range(sn):
                table_ij = table[si*sn:(si+1)*sn, sj*sn:(sj+1)*sn]
                mask_ij = mask[si*sn:(si+1)*sn, sj*sn:(sj+1)*sn]
                c += check_error (table_ij[mask_ij])

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
                    if k == 0:
                        sdk += '  '

                    else:
                        sdk += f'{k} '

                sdk += '| '

            if i in [h*sn-1 for h in range (1, sn)]:
                sdk += '\n-------------------------\n'

            else:
                sdk += '\n'

        print(sdk)

    def copy(self):
        return deepcopy(self)

def check_error(array):
    if array.size == 0:
        err = 0
    else:
        err = array.size-np.unique(array).size

    return err
