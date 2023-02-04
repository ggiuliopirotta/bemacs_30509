import numpy as np

def accept(c_delta, b):
    if c_delta <= 0:
        return True

    if b == np.inf:
        return False

    prob = np.exp(-b*c_delta)
    acc = np.random.random() < prob
    return acc

def sim_ann(prob, iters, b0, b1, ann_steps, seed=None):
    if seed is not None:
        np.random.seed(seed)

    best = None
    c_min = np.inf
    prob.init_config()
    c = prob.compute_cost()
    print(f'initial cost: {c}')

    b_list = np.zeros(ann_steps)
    b_list[:-1] = np.logspace(np.log10(b0), np.log10(b1), ann_steps-1)
    b_list[-1] = np.inf
    
    for b in b_list:
        acc = 0

        for _ in range(iters):
            move = prob.propose_move()
            c_delta = prob.compute_delta_cost(move)

            if accept(c_delta, b):
                prob.accept_move(move)
                c += c_delta
                acc += 1

                if c < c_min:
                    c_min = c
                    best = prob.copy()

                    if c == 0:
                        break

        print(f'beta: {b}, cost: {c}, acc. rate: {acc/iters}')
        if c == 0:
            break

    print(f'min cost: {c_min}')
    best.display()
    return best
