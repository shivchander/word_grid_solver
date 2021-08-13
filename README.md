# Find words from a word grid
My solution to solve the word grid problem - finding valid English words from a grid


## Given Problem

On a 4x4 board, find words that can be formed by a sequence of adjacent (top, bottom, left, right, diagonal) letters. 

Words must be 3 or more letters.

You may move to any of 8 adjacent letters, however, a word should not have multiple instances of the same cell.

Assume we have a list of all valid english words

## Solution

This problem can be broken down to two sub problems:

* Enumerating all possible strings from the grid
* Testing if the string is a valid word

To enumerate all the possible strings, we can iterate over all the cells in the board one by one, and from each cell 
we will move to any one of its neighbors and then repeat this. 
 
Or We can assume the board as a fully connected graph, and perform DFS from each node generate the words.

### Naive Solution

A Naive way of solving this would be to go from the list of all valid words to the grid.

* Iterate through the list of all valid words 
* for each word check if the word can be formed from the grid:
    * iterate through the board cells
    * if the cell matches with word start
        * explore its neighbors and move to the cell which matches the second letter
        * move to that cell and repeat these steps until the whole word matches

#### Computation Analysis

Time Complexity: 

Assume a grid of size (MxM), the longest word is of len K and wordlist of size N,

For each word in the word list, we need to check all the possible cells in the grid and start the walk from each cell.
And the walks can be of max len of k

Thus time complexity = O(N * M*M * k)

Space Complexity: O(N) to store the word list

#### Problems with Naive:

Clearly from the complexities, we can see that we can do much better than naive. The major contributor to the complexity
is the size of the word list. If we assume it to be English dictionary then N >> M and N >> k. So we would need to remove 
the dependency of this N. One way to do it would be to reverse the approach; move from grid to the wordlist. First generate
words from the grid and check its validity. 


### Trie-based Solution
In order to optimize the way we store and access the wordlist we can:

* Store the words in a hashset 
* Store the words in a Trie/Prefix tree

We can also use DFS with backtracking. And filter out words which don't start with letters not from the grid. 
This will help us prune out whole branches in a trie and remove words in the hashset.

‘Trie’ also known as a prefix tree is a tree data structure used to store character keys. Each node in the trie has 
children whose values (characters) lead to valid character keys.


## Performance Analysis:

![Performance](random_grid_performance.png)

This plot generates 100 random 3x3 grids and computes the time taken for each of the algorithm:

![Performance](random_sizes_performance.png)



### Observations:

* Naive is clearly less optimal than 


