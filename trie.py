#!/usr/bin/env python

"""trie.py: Description of what foobar does."""

__author__ = "Shivchander Sudalairaj"
__email__ = "sudalasr@mail.uc.edu"


class Trie:
    """
    Trie/Prefix Tree data structure to efficiently load the dictionary of all valid words
    https://en.wikipedia.org/wiki/Trie
    """

    def __init__(self, val='root'):             # null root
        self.val = val
        self.children = {}
        self.parent = None          # bidirectional pointers
        self.terminator = False     # flag denoting the end of the word

    def __repr__(self):
        return '<trie node representation>'

    def __str__(self, level=0):
        ret = "\t" * level + repr(self.val) + "\n"
        for child in self.children:
            ret += self.children[child].__str__(level+1)
        return ret

    def get_children(self):
        return self.children

    def insert_word(self, word):
        """
        :param word:
        :return:
        """
        curr_node = self
        for ch in word:
            if ch not in curr_node.children:
                new_node = Trie(ch)
                new_node.parent = curr_node
                curr_node.children[ch] = new_node
            curr_node = curr_node.children[ch]
        curr_node.terminator = word

    def word_exists(self, word):
        """
        :param word:
        :param prune:
        :return:
        """
        curr_node = self
        for ch in word:
            if ch not in curr_node.children:
                return False
            curr_node = curr_node.children[ch]

        return bool(curr_node.terminator)

    def prefix_exists(self, prefix):
        """
        :param prefix:
        :return:
        """
        curr_node = self
        for ch in prefix:
            if ch not in curr_node.children:
                return False
            curr_node =  curr_node.children[ch]
        return True
