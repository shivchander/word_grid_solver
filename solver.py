#!/usr/bin/env python

"""trie.py: Description of what foobar does."""

__author__ = "Shivchander Sudalairaj"
__email__ = "sudalasr@mail.uc.edu"


class Solver:
    def __init__(self, board, trie, dictionary, minlen):
        self.board = board
        self.trie = trie
        self.dictionary = dictionary
        self.rows = board.rows
        self.cols = board.cols
        self.minlen = minlen

    def dfs(self, i, j, visited, curr_word, words, opt):
        """
        :param i:
        :param j:
        :param visited:
        :param curr_word:
        :param words:
        :param opt:
        :return:
        """

        if (i, j) in visited:
            return
        ch = self.board.grid[i][j]
        visited.append((i, j))
        curr_word += ch
        if opt == 'hashset':
            if len(curr_word) >= self.minlen:
                if curr_word in self.dictionary:
                    words.append(curr_word)
        else:
            if self.trie.word_exists(curr_word):
                words.append(curr_word)

        neighbors = self.board.neighbors((i, j))
        for n in neighbors:
            self.dfs(neighbors[n][0], neighbors[n][1], visited[::], curr_word, words, opt)

    def naive_solve(self, wordlist):
        """
        :param wordlist:
        :return:
        """
        words = []
        for word in wordlist:
            if len(word) >= self.minlen:
                if self.board.word_exist(word):
                    words.append(word)

        return words

    def solve(self, opt='trie'):
        """
        :param opt:
        :return:
        """
        words = []
        for i in range(self.rows):
            for j in range(self.cols):
                self.dfs(i, j, [], '', words, opt=opt)

        return words
