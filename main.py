#!/usr/bin/env python

"""trie.py: Description of what foobar does."""

__author__ = "Shivchander Sudalairaj"
__email__ = "sudalasr@mail.uc.edu"

from board import Board
from trie import Trie
from solver import Solver
from itertools import chain
from collections import defaultdict
import time
import random
import string
import argparse

import matplotlib.pyplot as plt
import numpy as np


def load_grid(filename):
    """
    :param filename:
    :return:
    """
    return [list(line.rstrip('\n')) for line in open(filename)]


def random_grid(nrows, ncols):
    """
    :param nrows:
    :param ncols:
    :return:
    """
    grid = [[] for i in range(nrows)]
    for i in range(nrows):
        for j in range(ncols):
            grid[i].append(random.choice(string.ascii_letters.lower()))

    return grid


def build_trie(trie, word_list, unique_chars, word_len=0):
    """
    :param trie:
    :param word_list:
    :param unique_chars:
    :param word_len:
    :return:
    """
    for word in word_list:
        if len(word) >= word_len:
            if word[0] in unique_chars:
                trie.insert_word(word)


def build_wordlist(filename, filter=False):
    """
    :param filename:
    :return:
    """
    if filter:
        return [word.rstrip('\n') for word in open(filename) if word[0] in filter]
    else:
        return [word.rstrip('\n') for word in open(filename)]


def build_trie(trie, word_list, unique_chars, word_len=3):
    """
    :param trie:
    :param word_list:
    :param unique_chars:
    :param word_len:
    :return:
    """
    for word in word_list:
        if len(word) >= word_len:
            if word[0] in unique_chars:
                trie.insert_word(word)


def solve_grid(grid, word_len, opt):
    """
    :param grid:
    :param word_len:
    :param opt:
    :return:
    """
    b = Board(grid)
    t = Trie()
    out = defaultdict(dict)

    unique_characters = ''.join(set(chain.from_iterable(grid)))
    wordlist = build_wordlist('wordlist.10000.txt')
    trie_words = build_wordlist('wordlist.10000.txt', filter=unique_characters)

    build_trie(t, trie_words, unique_characters, word_len=word_len)
    s = Solver(b, minlen=word_len)

    if opt == 'trie' or opt == 'both':
        start = time.time()
        out['trie']['res'] = s.trie_solve(t)
        end = time.time()
        out['trie']['time'] = end - start

    if opt == 'naive' or opt == 'both':
        start = time.time()
        out['naive']['res'] = s.naive_solve(wordlist)
        end = time.time()
        out['naive']['time'] = end - start

    return out


def test_random_grids(args):
    naive_times = []
    trie_times = []
    for i in range(args.test_size):
        grid = random_grid(args.size, args.size)
        res = solve_grid(grid, 3, opt='both')
        naive_times.append(res['naive']['time'])
        trie_times.append(res['trie']['time'])

    print('Average Times: \n')
    print('naive: {}'.format(np.mean(np.array(naive_times))))
    print('trie: {}'.format(np.mean(np.array(trie_times))))

    plt.plot(np.arange(args.test_size), naive_times, label='naive')
    plt.plot(np.arange(args.test_size), trie_times, label='trie')
    plt.title('Comparison of time taken for each algo with random {}x{} grid'.format(args.size, args.size))
    plt.legend()
    plt.xlabel('Random Sample #')
    plt.ylabel('Time Taken')

    plt.savefig('random_grid_performance.png')
    plt.clf()


def test_random_grid_sizes(args):
    """
    :param args:
    :param algo:
    :return:
    """
    naive_times = []
    trie_times = []
    for i in range(2, args.test_max_gridsize+1):
        grid = random_grid(i, i)
        res = solve_grid(grid, 3, opt='both')
        naive_times.append(res['naive']['time'])
        trie_times.append(res['trie']['time'])

    plt.plot(np.arange(2, args.test_max_gridsize+1), naive_times, label='naive')
    plt.plot(np.arange(2, args.test_max_gridsize+1), trie_times, label='trie')
    plt.title('Comparison of time taken for each algo with varying grid size')
    plt.legend()
    plt.xlabel('Grid Size')
    plt.ylabel('Time Taken')

    plt.savefig('random_sizes_performance.png')
    plt.clf()


def get_args():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description='Find words in a Grid of letters')
    parser.add_argument('-default', default=False, help="solve default board stored in grid.txt")
    parser.add_argument('-random', default=False, help="solve a random board")
    parser.add_argument('-test', default=True, help="test performance")
    parser.add_argument('-size', default=4, type=int, help="board size")
    parser.add_argument('-test_size', default=100, type=int, help="# of experiments to run")
    parser.add_argument('-test_max_gridsize', default=10, type=int, help="maximum grid size")
    parser.add_argument('-opt', default="both", type=str, help="trie/naive/both")
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    args = get_args()
    if args.default:
        grid = load_grid('grid.txt')
        print('Grid: ')
        print(np.array(grid))
        res = solve_grid(grid, 3, opt=args.opt)
        print()
        for algo in res:
            print('Algo: {}'.format(algo))
            print('\t Result: {}'.format(sorted(res[algo]['res'])))
            print('\t Num of Words: {}'.format(len(res[algo]['res'])))
            print('\t Time: {}'.format(res[algo]['time']))
            print()

    if args.random:
        grid = random_grid(args.size, args.size)
        print('Grid: ')
        print(np.array(grid))
        res = solve_grid(grid, 3, opt=args.opt)
        print()
        for algo in res:
            print('Algo: {}'.format(algo))
            print('\t Result: {}'.format(sorted(res[algo]['res'])))
            print('\t Num of Words: {}'.format(len(res[algo]['res'])))
            print('\t Time: {}'.format(res[algo]['time']))
            print()

    if args.test:
        test_random_grids(args)
        test_random_grid_sizes(args)
