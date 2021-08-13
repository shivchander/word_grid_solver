#!/usr/bin/env python

"""trie.py: Description of what foobar does."""

__author__ = "Shivchander Sudalairaj"
__email__ = "sudalasr@mail.uc.edu"

import numpy as np


class Board:
    def __init__(self, grid):
        self.grid = np.array(grid)
        self.rows, self.cols = self.grid.shape

    def __repr__(self):
        return '<board>'

    def __str__(self, level=0):
        return str(self.grid)

    def neighbors(self, pos):
        """
        :param pos:
        :return:
        """
        i, j = pos
        dis = [0, 1, 1, 1, 0, -1, -1, -1]
        djs = [-1, -1, 0, 1, 1, 1, 0, -1]

        return [(i+di, j+dj) for di, dj in zip(dis, djs)
                if 0 <= i + di < self.rows and 0 <= (j + dj) < self.cols]

    def backtrack(self, i, j, suffix, curr_grid):
        """
        :param i:
        :param j:
        :param suffix:
        :return:
        """
        # base case
        if len(suffix) == 0:
            return True

        if curr_grid[i][j] != suffix[0]:
            return False

        ret = False
        curr_grid[i][j] = '#'

        neighbors = self.neighbors((i, j))
        for (ix, jx) in neighbors:
            if curr_grid[ix][jx] != '#':
                ret = self.backtrack(ix, jx, suffix[1:], curr_grid)
                if ret:
                    break

        curr_grid[i][j] = suffix[0]

        return ret

    def word_exist(self, word):
        """
        :param word:
        :return:
        """
        curr_grid = self.grid.copy()
        for i in range(self.rows):
            for j in range(self.cols):
                if curr_grid[i][j] == word[0]:
                    if self.backtrack(i, j, word, curr_grid):
                        return True

        return False
