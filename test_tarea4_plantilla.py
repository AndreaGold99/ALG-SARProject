import numpy as np
from trie import Trie
import time
import pdb

def dp_levenshtein_trie(x, trie, th):
    states = trie.get_num_states()
    current = np.zeros(states)
    previous = np.zeros(states)
    
    for c in range(1, len(current)):
        # Mira quien es el padre del estado c
        index = trie.get_parent(c)
        # Lo que me cuesta
        current[c] = current[index] + 1
    
    for letter in x:
        previous, current = current, previous
        current[0] = previous[0] + 1
        for st in range(1,trie.get_num_states()):
            parent = trie.get_parent(st)
            current[st] = min(
                current[parent] + 1,
                previous[st] + 1,
                previous[parent] + (letter != trie.get_label(st)),
            )
        if min(current) > th:
            return {}
    
    aux = {
        trie.get_output(st): current[st]
        for st in range(trie.get_num_states())
        if trie.is_final(st) and current[st] <= th
    }
    return aux


def dp_restricted_damerau_trie(x, trie, th):
    states = trie.get_num_states()
    current = np.zeros(states)
    previous = np.zeros(states)
    previous2 = np.zeros(states)
    for c in range(1, len(current)):
        current[c] = current[trie.get_parent(c)] + 1
    last = -4
    for letter in x:
        previous, current, previous2 = current, previous2, previous
        current[0] = previous[0] + 1
        for st in range(1,states):
            parent = trie.get_parent(st)
            if parent > 0 and last == trie.get_label(st) and letter == trie.get_label(parent):
                aux = previous2[trie.get_parent(parent)] + 1
            else: 
                aux = 10000
            current[st] = min(current[parent] + 1,
                previous[st] + 1,
                previous[parent] + (letter != trie.get_label(st)),
                aux)

        if min(current) > th:
                return []
        last = letter
    return [
        (trie.get_output(st),current[st])
        for st in range(trie.get_num_states())
        if trie.is_final(st) and current[st] <= th
    ]


def dp_intermediate_damerau_trie(x, trie, th):
    states = trie.get_num_states()
    current = np.zeros(states)
    previous = np.zeros(states)
    previous2 = np.zeros(states)
    previous3 = np.zeros(states)
    for c in range(1, len(current)):
        current[c] = current[trie.get_parent(c)] + 1
    for l in range(len(x)):
        previous, current, previous2 = current, previous2, previous
        current[0] = previous[0] + 1
        for st in range(1,states):
            parent = trie.get_parent(st)
            parent2 = trie.get_parent(parent)
            current[st] = min(current[parent] + 1,
                previous[st] + 1,
                previous[parent] + (x[l] != trie.get_label(st)))
            if x[l] == "b":
                pdb.set_trace()
            if parent > 0 and x[l-1] == trie.get_label(st) and x[l]== trie.get_label(parent):
                current[st] = min(previous[parent2] + 1,current[st])
                
            if l > 1 and parent2 > -1 and x[l-1] == trie.get_label(st) and x[l] == trie.get_label(parent2):
                current[st] = min(previous2[parent2] + 2,current[st])
                
            if l > 1 and parent > 0 and x[l-2] == trie.get_label(st) and x[l] == trie.get_label(parent):
                current[st] = min(previous[parent2] + 2, current[st])
        if min(current) > th:
                return []
    return [
        (trie.get_output(st),current[st])
        for st in range(trie.get_num_states())
        if trie.is_final(st) and current[st] <= th
    ]

words = ["ba"]
#["algortimo","algortximo", "lagortimo", "agaloritom", "algormio", "ba"]


words.sort()
trie = Trie(words)

test = ["acb","algoritmo"]
thrs = range(1, 4)
for threshold in thrs:
    print(f"threshols: {threshold:3}")
    for x in test:
        for dist, name in (
            #(dp_levenshtein_trie, "levenshtein"),
            #(dp_restricted_damerau_trie, "restricted"),
            (dp_intermediate_damerau_trie, "intermediate"),
        ):
            dist(x, trie, threshold)
            print(f"\t{x:12} \t{name}\t", end="")
            print(dist(x, trie, threshold))

"""
Salida del programa:

threshols:   1
    algoritmo    	levenshtein	[]
    algoritmo    	restricted	[('algortimo', 1)]
    algoritmo    	intermediate	[('algortimo', 1)]
    acb          	levenshtein	[]
    acb          	restricted	[]
    acb          	intermediate	[]
threshols:   2
    algoritmo    	levenshtein	[('algortimo', 2)]
    algoritmo    	restricted	[('algortimo', 1), ('lagortimo', 2)]
    algoritmo    	intermediate	[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('algortximo', 2)]
    acb          	levenshtein	[]
    acb          	restricted	[]
    acb          	intermediate	[('ba', 2)]
threshols:   3
    algoritmo    	levenshtein	[('algormio', 3), ('algortimo', 2), ('algortximo', 3)]
    algoritmo    	restricted	[('algormio', 3), ('algortimo', 1), ('lagortimo', 2), ('algortximo', 3)]
    algoritmo    	intermediate[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('agaloritom', 3), ('algortximo', 2)]
    acb          	levenshtein	[('ba', 3)]
    acb          	restricted	[('ba', 3)]
    acb          	intermediate	[('ba', 2)]

"""
