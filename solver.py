#!/usr/bin/env python

"""
solver.py: contains the Solver class and its trie solve and naive solve functions

This solves the word finder problem by using a naive method and then an optimized trie method
"""

__author__ = "Shivchander Sudalairaj"
__email__ = "sudalasr@mail.uc.edu"


class Solver:
    def __init__(self, board, minlen=3):
        self.board = board
        self.rows = board.rows
        self.cols = board.cols
        self.minlen = minlen

    def trie_solve(self, trie, prune=True):
        """
        solves the word finder from grid using a dfs walk on the grid to generate possible strings and validates it
        bu checking its existence in the trie

        here we are parallely walking on both the grid and trie at the same time. Thus we dont search from the root of
        the trie everytime. This saves a bunch of computes. The tree is also being pruned once the word is found.

        :param trie: trie obj - fully built trie which stores the filtered english words
        :param prune: bool - whether to prune the tree once the word is found
        :return: list - list of words valid found in the grid
        """
        def dfs(i, j, trie_node, prune):

            ch = grid[i][j]
            curr_node = trie_node[ch]

            # check if curr_node is the end of the word
            curr_node_val = curr_node.pop(terminator, False)
            if curr_node_val:
                if len(curr_node_val) >= minlen:
                    words.append(curr_node_val)

            # marking the board state as visited
            grid[i][j] = '$'

            neighbors = board.neighbors((i, j))
            for (i_hat, j_hat) in neighbors:
                if grid[i_hat][j_hat] == '$':
                    continue
                if not grid[i_hat][j_hat] in curr_node:
                    continue
                dfs(i_hat, j_hat, curr_node, prune)

            # end of walk, mark the cells as unvisted
            grid[i][j] = ch

            # pruning
            if prune:
                if not curr_node:
                    trie_node.pop(ch)

        words = []
        board = self.board
        terminator = trie.terminator
        trie = trie.trie
        minlen = self.minlen
        grid = self.board.grid
        rows = self.rows
        cols = self.cols

        for row in range(rows):
            for col in range(cols):
                # check if there are words starting from this cell ch
                if grid[row][col] in trie:
                    dfs(row, col, trie, prune)

        return words

    def naive_solve(self, wordlist):
        """
        solves the word grid problem with a naive method - This goes from the list of words to the grid.

        The algorithm traverses through a list of unfiltered words. And for each word it checks whether it can be formed
        from the grid.

        :param wordlist: list - list of unfiltered words
        :return: list - list of words valid found in the grid
        """
        words = []
        for word in wordlist:
            if len(word) >= self.minlen:
                if self.board.word_exist(word):
                    words.append(word)
        return words
