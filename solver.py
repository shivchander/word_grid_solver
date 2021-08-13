#!/usr/bin/env python

"""trie.py: Description of what foobar does."""

__author__ = "Shivchander Sudalairaj"
__email__ = "sudalasr@mail.uc.edu"


class Solver:
    def __init__(self, board, minlen=3):
        self.board = board
        self.rows = board.rows
        self.cols = board.cols
        self.minlen = minlen

    def trie_solve(self, trie, prune=True):
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
                if grid[i_hat][j_hat] == '#':
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
        words = []
        for word in wordlist:
            if len(word) >= self.minlen:
                if self.board.word_exist(word):
                    words.append(word)
        return words
