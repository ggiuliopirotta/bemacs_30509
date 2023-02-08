from Sudoku Import import Sdk_Import
from Sudoku Generator import Sdk_Generator
from Sudoku Solver import Sdk_Solver

from Greedy import greedy
from Simulated Annealing import sim_ann

sdk_gen = Sdk_Generator(n=9, r=0.1)
sdk_gen.display()

sdk_sol = Sdk_Solver(sdk_gen)
sim_ann(sdk_sol, iters=1000, b0=2, b1=100, ann_steps=30)
