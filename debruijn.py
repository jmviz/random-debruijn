# https://en.wikipedia.org/wiki/De_Bruijn_sequence
# https://en.wikipedia.org/wiki/De_Bruijn_graph
# https://en.wikipedia.org/wiki/Eulerian_path

import random
import numpy as np
import string
import itertools

def generate_subsequences(k, n):
    """List of all possible subsequences of length n with alphabet of size k"""
    alphabet = [[i] for i in range(k)]
    a = alphabet
    for _ in range(n-1):
        a = [i + j for i in a for j in alphabet]
    return a

class DeBruijnGraph:
    def __init__(self, k, n):
        """Generate n-dimensional de Bruijn graph over k symbols.

        The graph is represented by its adjacency matrix.
        Also stores all subsequences of length n over k symbols, i.e. the nodes of the graph.

        E.g. g = DeBruijnGraph(2, 2)
        g.matrix: [[1,1,0,0],[0,0,1,1],[1,1,0,0],[0,0,1,1]]
        g.subsequences: ['00','01','10','11']
        """
        self.k = k
        self.n = n
        subsequences = generate_subsequences(k, n)
        self.subsequences = subsequences
        self.order = len(subsequences) # number of nodes
        size = 0
        matrix = []
        for i, subsequence1 in enumerate(subsequences):
            row = []
            for j, subsequence2 in enumerate(subsequences):
                if subsequence1[1:] == subsequence2[:n-1]:
                    row.append(1)
                    size += 1
                else:
                    row.append(0)
            matrix.append(row)
        self.size = size # number of edges
        self.matrix = np.array(matrix) # adjacency matrix
    def euler_cycle(self, f = 1):
        """
        Hierholzer's algorithm for Euler cycle in de Bruijn graph.
        If f > 1, then if node1 -> node2, then there are f such directed edges.
        """
        m = np.copy(self.matrix) * f
        cycle = [] # list of visited nodes in order
        cycle.append(random.randint(0, self.order - 1))
        while np.count_nonzero(m) > 0:
            subcycle = []
            u = np.unique(cycle)
            p = np.random.choice(u[np.sum(m[u],1) > 0])
            subcycle.append(p)
            while subcycle[0] != subcycle[-1] or len(subcycle) < 2:
                subcycle.append(np.random.choice(np.where(m[subcycle[-1]]>0)[0]))
                m[subcycle[-2],subcycle[-1]] -= 1
            index = 1 + np.random.choice([i for i,t in enumerate(cycle) if t==p])
            cycle[index:index] = subcycle[1:]
        return cycle
    def debruijn_sequence(self, f = 1):
        """f-fold de Bruijn sequence as list of numbers"""
        s = self.subsequences
        cycle = self.euler_cycle(f)
        sequence = []
        for node in cycle[:-1]:
            sequence.append(s[node][-1])
        return sequence
    def debruijn_string(self, f = 1):
        """String representation of f-fold de Bruijn sequence"""
        k = self.k
        all_chars = string.digits + string.ascii_letters
        if k > len(all_chars):
            print("Number of symbols (k) too great, use debruijn_sequence().")
            return
        else:
            chars = all_chars[:k]
        sequence = self.debruijn_sequence(f)
        return ''.join([chars[c] for c in sequence])

class Sequencer:
    def __init__(self, n, *args):
        """
        n indicates length of trial-type subsequences to be balanced.
        Each arg should list of levels of a factor.
        E.g.:
            probe_congruence = [True, False]
            orientations = ["left", "right"]
            sequencer = Sequencer(2, probe_congruence, orientations)
            block = sequencer.block()
            for trial in block: probe_congruent, orientation = trial
        """
        self.n = n
        trial_types = list(itertools.product(*args))
        self.trial_types = trial_types
        self.graph = DeBruijnGraph(len(trial_types),n-1)
    def block(self, f = 1, append = None):
        """
        A canonical f-fold de Bruijn sequence is length f*k^n and contains the same
        number (f*k^(n-1)) of each symbol (here, each trial type). However,
        there are n-1 trial type subsequences that will appear f-1 times if one
        proceeds through the sequence and stops at the end rather than wrapping
        around to the beginning again. Setting append = "end" will slightly
        unbalance the number of each trial type, by appending the first n-1 trial
        types to the end of the sequence, so that each trial type subsequence
        occurs f times in each block if it is traversed in a non-wraparound way.
        Similarly, append = "start" will append the last n-1 trial types to the start
        of the sequence. This would be useful if you intend to use a different trial type
        ordering in each block, or intend for an entire session to be only one
        block. Ignore this parameter if you want to have your block be a canonical
        de Bruijn sequence.
        """
        sequence = self.graph.debruijn_sequence(f)
        b = [self.trial_types[s] for s in sequence]
        if append == "end":
            return b + b[:self.n-1]
        elif append == "start":
            return b[-(self.n-1):] + b
        else:
            return b

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Generate random debruijn string.')
    parser.add_argument('k', type = int, help='alphabet size')
    parser.add_argument('n', type = int, help='order of the debruijn string')
    parser.add_argument('-f', type = int, required=False, default=1, help='f-fold debruijn string')
    args = parser.parse_args()

    g = DeBruijnGraph(args.k, args.n-1)
    print(g.debruijn_string(args.f))
