import numpy as np
from trie import Trie
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
                return {}
        last = letter
    return {
        trie.get_output(st):current[st]
        for st in range(trie.get_num_states())
        if trie.is_final(st) and current[st] <= th
    }


def dp_intermediate_damerau_trie(y, trie, th):
    states = trie.get_num_states()
    current = np.zeros(states)
    previous = np.zeros(states)
    previous2 = np.zeros(states)
    previous3 = np.zeros(states)
    for c in range(1, len(current)):
        current[c] = current[trie.get_parent(c)] + 1
    for j in range(len(y)):
        previous, previous2, previous3, previous3, current  = current, previous, previous2, previous2, previous3
        current[0] = previous[0] + 1
        for i in range(1,states):

            parent = trie.get_parent(i)
            current[i] = min(current[parent] + 1,
                previous[i] + 1,
                previous[parent] + (y[j] != trie.get_label(i)))
            
            if parent > 0 and j > 0:
                parent2 = trie.get_parent(parent)
                parent2 = trie.get_parent(parent)
                if y[j-1] == trie.get_label(i) and y[j]== trie.get_label(parent):
                    current[i] = min(previous2[parent2] + 1,current[i])
                
                if y[j-1] == trie.get_label(i) and y[j] == trie.get_label(parent2):
                    current[i] = min(previous2[trie.get_parent(parent2)] + 2,current[i])
                
                if j > 1 and y[j-2] == trie.get_label(i) and y[j] == trie.get_label(parent):
                    current[i] = min(previous3[parent2] + 2, current[i])
        if min(current) > th:
                return {}
    
    return {
        trie.get_output(st):current[st]
        for st in range(trie.get_num_states())
        if trie.is_final(st) and current[st] <= th
    }

words = ["algortimo","algortximo", "lagortimo", "agaloritom", "algormio", "ba"]


words.sort()
trie = Trie(words)

test = ["algoritmo","acb"]
thrs = range(1, 4)
for threshold in thrs:
    print(f"threshols: {threshold:3}")
    for x in test:
        for dist, name in (
            (dp_levenshtein_trie, "levenshtein"),
            (dp_restricted_damerau_trie, "restricted"),
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
