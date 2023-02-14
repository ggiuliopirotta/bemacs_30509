import matplotlib.pyplot as plt
import numpy as np

def greedy(prob, iters, restarts, plot=True, seed=None):
    if seed is not None:
        np.random.seed(seed)

    e_pairs = prob.couple_edges()
    best = None
    c_min = np.inf

    for _ in range(restarts):
        prob.init_config()
        c = prob.compute_cost()
        print(f'initial cost: {c}')

        for _ in range (iters):
            move_best = None
            c_delta_min = np.inf

            for move in e_pairs:
                c_delta = prob.compute_delta_cost(move)
    
                if c_delta < c_delta_min:
                    move_best = move
                    c_delta_min = c_delta

            prob.accept_move(move_best)
            c += c_delta_min

            if plot:
                prob.display()

        if c < c_min:
            c_min = c
            best = prob.copy()
    
    print (f'min cost: {c_min}')
    best.display()
    plt.show()
    return best
