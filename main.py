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


def build_hashset(filename, unique_chars, word_len=0):
    """
    :param filename:
    :param unique_chars:
    :param word_len:
    :return:
    """
    dict_set = set()
    for word in open(filename):
        word = word.rstrip('\n')
        if len(word) >= word_len:
            if word[0] in unique_chars:
                dict_set.add(word)

    return dict_set


def build_wordlist(filename):
    """
    :param filename:
    :return:
    """
    return [word.rstrip('\n') for word in open(filename)]


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
    dict_set = build_hashset('wordlist.10000.txt', unique_characters)
    wordlist = build_wordlist('wordlist.10000.txt')

    build_trie(t, dict_set, unique_characters, word_len=word_len)
    s = Solver(b, t, dict_set, minlen=word_len)

    if opt == 'hashset' or opt == 'all':
        start = time.time()
        out['hashset']['res'] = s.solve(opt='hashset')
        end = time.time()
        out['hashset']['time'] = end - start

    if opt == 'trie' or opt == 'all':
        start = time.time()
        out['trie']['res'] = s.solve(opt='trie')
        end = time.time()
        out['trie']['time'] = end - start

    if opt == 'naive' or opt == 'all':
        start = time.time()
        out['naive']['res'] = s.naive_solve(wordlist)
        end = time.time()
        out['naive']['time'] = end - start

    return out


def test_random_grids(args):
    naive_times = []
    hashset_times = []
    trie_times = []
    for i in range(args.test_size):
        grid = random_grid(args.size, args.size)
        res = solve_grid(grid, 3, opt=args.opt)
        naive_times.append(res['naive']['time'])
        hashset_times.append(res['hashset']['time'])
        trie_times.append(res['trie']['time'])

    print('Average Times: \n')
    print('naive: {}'.format(np.mean(np.array(naive_times))))
    print('hashset: {}'.format(np.mean(np.array(hashset_times))))
    print('trie: {}'.format(np.mean(np.array(trie_times))))

    plt.plot(np.arange(args.test_size), naive_times, label='naive')
    plt.plot(np.arange(args.test_size), hashset_times, label='hashset')
    plt.plot(np.arange(args.test_size), trie_times, label='trie')
    plt.title('Comparison of time taken for each algo')
    plt.legend()
    plt.xlabel('Random Sample #')
    plt.ylabel('Time Taken')

    plt.savefig('performance.png')


def test_random_grid_sizes(args, algo='trie'):
    """
    :param args:
    :param algo:
    :return:
    """
    times = []
    for i in range(2, args.test_max_gridsize+1):
        grid = random_grid(i, i)
        start = time.time()
        res = solve_grid(grid, 3, opt=args.opt)
        end = time.time()
        times.append(end - start)

    plt.plot(np.arange(args.test_max_gridsize), times)
    plt.title('Time taken by {} with varying grid size'.format(algo))
    plt.xlabel('Grid Size')
    plt.ylabel('Time Taken')
    plt.savefig('{}.png'.format(algo))


def get_args():
    """
    :return:
    """
    parser = argparse.ArgumentParser(description='Find words in a Grid of letters')
    parser.add_argument('-default', default=True, help="solve default board stored in grid.txt")
    parser.add_argument('-random', default=False, help="solve a random board")
    parser.add_argument('-test', default=False, help="test performance")
    parser.add_argument('-size', default=3, type=int, help="board size")
    parser.add_argument('-test_size', default=100, type=int, help="# of experiments to run")
    parser.add_argument('-test_max_gridsize', default=5, type=int, help="maximum grid size")
    parser.add_argument('-opt', default="trie", type=str, help="trie/hashset/naive/all")
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
            print('\t Time: {}'.format(res[algo]['time']))
            print()

    if args.test:
        test_random_grids(args)
