import matplotlib.pyplot as plt
import numpy as np

def display_walks(grid_size, n_walkers, coord, coord_old):
    plt.pause(0.1)
    plt.figure(1)
    plt.clf()

    for i in range(grid_size):
        plt.plot([0, grid_size-1], [i,i], color='grey', alpha=0.7)
        plt.plot([i,i], [0, grid_size-1], color='grey', alpha=0.7)

    x, y = coord[:,0], coord[:,1]
    x_old, y_old = coord_old[:,0], coord_old[:,1]

    for j in range(n_walkers):
        if abs(x_old[j]-x[j]) == grid_size-1 or abs(y_old[j]-y[j]) == grid_size-1:
            continue

        plt.plot([x_old[j], x[j]], [y_old[j], y[j]], color='orange', linewidth=3, alpha=0.7)

    plt.plot(x, y, 'o', color='red', markersize=10, alpha=1/np.sqrt(n_walkers))

def display_prob(grid_size, prob_marg):
    plt.pause(0.1)
    plt.figure(2)
    plt.clf()
    plt.pcolormesh(prob_marg.reshape((grid_size, grid_size)), cmap='Greys')

def random_walks(grid_size, n_walkers, iters, plot_prob):
    moves = np.array([[1,0], [-1,0], [0,1], [0,-1]])
    n_moves = len(moves)
    prob = np.array([1/4, 1/4, 1/4, 1/4])

    coord = np.zeros((n_walkers, 2), dtype=int)
    coord[:,1].fill(grid_size//2)
    coord[:,0].fill(grid_size//2)

    prob_marg = np.zeros(grid_size**2)
    prob_marg[grid_size//2 + grid_size*(grid_size//2)] = 1
    Q = np.zeros((grid_size**2, grid_size**2))

    for i in range(grid_size**2):
        j = i//grid_size
        k = i%grid_size

        for m, p in zip(moves, prob):
            jNew = (j+m[1])%grid_size
            kNew = (k+m[0])%grid_size
            Q[grid_size*jNew+kNew, i] += p

    for _ in range(iters):
        coord_old = coord.copy()
        coord += moves[np.random.choice(n_moves, n_walkers, p=prob)]
        coord %= grid_size
        prob_marg = Q@prob_marg
        display_walks(grid_size, n_walkers, coord, coord_old)

        if plot_prob:
            display_prob(grid_size, prob_marg)

    print(prob_marg)
    plt.show()

random_walks(grid_size=20, n_walkers=20, iters=100, plot_prob=False)
