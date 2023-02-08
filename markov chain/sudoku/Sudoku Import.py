from copy import deepcopy
import numpy as np

class Sdk_Creator:
    def __init__(self, table, mask):
        self.n = len(table)
        self.sn = int(np.sqrt(self.n))

        self.table = table-1
        self.mask = mask

    def __repr__(self):
        return str(self.table)

    def __add__(self, num):
        return self.table+num

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
