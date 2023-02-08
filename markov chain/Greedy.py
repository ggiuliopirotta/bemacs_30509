import numpy as np

def greedy(prob, iters, restarts, seed=None):
    if seed is not None:
        np.random.seed(seed)

    best = None
    c_min = np.inf

    for _ in range(restarts):
        prob.init_config()
        c = prob.compute_cost()
        print(f'initial cost: {c}')

        for _ in range(iters):
            move = prob.propose_move()
            c_delta = prob.compute_delta_cost(move)

            if c_delta <= 0:
                prob.accept_move(move)
                c += c_delta

            if c == 0:
                break

        if c < c_min:
            c_min = c
            best = prob.copy()

            if c == 0:
                break
    
    print (f'min cost: {c_min}')
    best.display()
    return best
