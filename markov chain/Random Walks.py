import matplotlib.pyplot as plt
import numpy as np

class Random_Walks:
    def __init__(self, n_walkers, size):
        self.n_walkers = n_walkers
        self.size = size
        self.p_marg = np.zeros(size**2)

    def go_random(self, iters, show_prob=False):
        n_walkers, size = self.n_walkers, self.size

        moves = np.array([[1,0], [-1,0], [0,1], [0,-1]])
        p = np.array([1/4, 1/4, 1/4, 1/4])

        coord = np.zeros((n_walkers, 2))
        coord[:,1] = size//2
        coord[:,0] = size//2
        self.p_marg[size//2+size*(size//2)] = 1

        Q = np.zeros((size**2, size**2))

        for i in range(size**2):
            j = i//size
            k = i %size

            for m_i, p_i in zip(moves, p):
                j_new = (j+m_i[1]) %size
                k_new = (k+m_i[0]) %size
                Q[size*j_new+k_new, i] += p_i

        for _ in range(iters):
            coord_old = coord.copy()
            coord += moves[np.random.choice(len(moves), n_walkers, p=p)]
            coord %= size
            self.p_marg = Q@self.p_marg
            self.display_walks(coord, coord_old)

            if show_prob:
                self.display_prob()

        print(self.p_marg)
        plt.show()

    def display_walks(self, coord, coord_old):
        n_walkers, size = self.n_walkers, self.size

        plt.pause(0.1)
        plt.figure(1)
        plt.clf()

        for i in range(size):
            plt.plot([0, size-1], [i,i], color='grey', alpha=0.7)
            plt.plot([i,i], [0, size-1], color='grey', alpha=0.7)

        x, y = coord[:,0], coord[:,1]
        x_old, y_old = coord_old[:,0], coord_old[:,1]

        for j in range(n_walkers):
            if abs(x_old[j]-x[j]) == size-1 or abs(y_old[j]-y[j]) == size-1:
                continue

            plt.plot([x_old[j], x[j]], [y_old[j], y[j]], color='orange', linewidth=3, alpha=0.7)

        plt.plot(x, y, 'o', color='red', markersize=10, alpha=1/np.sqrt(n_walkers))

    def display_prob(self):
        p_marg, size = self.p_marg, self.size

        plt.pause(0.1)
        plt.figure(2)
        plt.clf()

        plt.pcolormesh(p_marg.reshape((size, size)), cmap='Greys')

rnd_walks = Random_Walks(n_walkers=20, size=20)
rnd_walks.go_random(iters=50, show_prob=False)
