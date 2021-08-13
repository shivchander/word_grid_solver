#!/usr/bin/env python

"""
trie.py: contains the definition and declaration of the trie class
"""

__author__ = "Shivchander Sudalairaj"
__email__ = "sudalasr@mail.uc.edu"


class Trie:
    """
    Trie/Prefix Tree data structure to efficiently load the dictionary of all valid words
    https://en.wikipedia.org/wiki/Trie
    """

    def __init__(self):
        self.trie = {}
        self.terminator = '$'

    def insert_word(self, word):
        """
        inserts a word as a new branch or updates a branch to the trie

        :param word: str - word to be added
        :return: None
        """
        curr_node = self.trie
        for letter in word:
            curr_node = curr_node.setdefault(letter, {})
        curr_node[self.terminator] = word

    def word_exists(self, word):
        """
        walks through the trie to check if the word is present

        :param word: word to be searched
        :return: bool - whether the word is found
        """
        curr_node = self.trie
        for ch in word:
            if ch not in curr_node:
                return False
            curr_node = curr_node[ch]

        if self.terminator in curr_node:
            return curr_node['$'] == word
        else:
            return False
