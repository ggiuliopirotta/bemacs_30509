import matplotlib.pyplot as plt
import numpy as np

class Game_Of_Life:
    def __init__(self, size):
        self.board = np.zeros((size, size))
        self.size = size

    def config_rnd(self, p):
        size = self.size

        self.board = np.array(np.random.rand(size, size) < p, dtype=int)

    def play(self, turns):
        size = self.size

        for _ in range(turns):
            board = self.board
            nearest = np.zeros((size, size))

            for i in range(size):
                row_i = np.zeros(size)

                for j in range(size):
                    row_i[j] = np.sum(board[max(i-1, 0):min(i+2, size), max(j-1, 0):min(j+2, size)]) - board[i, j]

                nearest[i] = row_i

            alive = board*nearest
            alive[alive >= 4] = 0
            alive[alive <= 2] = 0
            alive[alive != 0] = 1

            dead = (board == 0)*nearest
            dead[dead < 3] = 0
            dead[dead != 0] = 1

            self.board = alive+dead
            self.display()

    def display(self):
        board, size = self.board, self.size

        plt.pause(0.1)
        plt.figure(1, figsize=(7, 7))
        plt.clf()

        for i in range(size):
            plt.plot([-1, size], [i-0.5, i-0.5], color='grey', alpha=0.7)
            plt.plot([i-0.5, i-0.5], [-1, size], color='grey', alpha=0.7)

        plt.imshow(board, cmap='Greys')

game = Game_Of_Life(size=20)
game.config_rnd(p=0.25)
game.play(turns=100)
plt.show()
