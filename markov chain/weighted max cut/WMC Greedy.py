import matplotlib.pyplot as plt
import numpy as np

def greedy (prob, iters, restarts, plot=False, seed=None):
    if seed is not None:
        np.random.seed (seed)

    best = None
    w_max = 0.0

    for _ in range(restarts):
        prob.init_config()
        w = prob.compute_cost()
        print(f'initial weight: {w}')

        for _ in range(iters):
            move = prob.propose_move()
            w_delta = prob.compute_delta_cost(move)

            if w_delta > 0:
                prob.accept_move(move)
                w += w_delta

                if plot:
                    prob.display()

        if w > w_max:
            w_max = w
            best = prob.copy()
    
    print(f'max weight: {w_max}')
    best.display()
    plt.show ()
    return best
