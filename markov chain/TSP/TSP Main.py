import Tsp
import Tsp_Greedy

tsp = Tsp.Tsp(n=100)
Tsp_Greedy.greedy(tsp, iters=110, restarts=1, plot=True)
