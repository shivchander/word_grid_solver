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

        return {self.grid[i+di][j+dj]: (i+di, j+dj) for di, dj in zip(dis, djs)
                if 0 <= i + di < self.rows and 0 <= (j + dj) < self.cols}

    def backtrack(self, i, j, suffix):
        """
        :param i:
        :param j:
        :param suffix:
        :return:
        """
        # base case
        if len(suffix) == 0:
            return True

        if self.grid[i][j] != suffix[0]:
            return False

        ret = False
        self.grid[i][j] = '#'

        neighbors = self.neighbors((i, j))
        for n in neighbors:
            ret = self.backtrack(neighbors[n][0], neighbors[n][1], suffix[1:])
            if ret:
                break
        self.grid[i][j] = suffix[0]

        return ret

    def word_exist(self, word):
        """
        :param word:
        :return:
        """
        for row in range(self.rows):
            for col in range(self.cols):
                if self.backtrack(row, col, word):
                    return True

        return False
