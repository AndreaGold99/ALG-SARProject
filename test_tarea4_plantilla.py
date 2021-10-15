import numpy as np
from trie import Trie

def dp_levenshtein_trie(x, trie, th):
	current = [0] * trie.get_num_states()
	previous = [0] * trie.get_num_states()

	for c in range(1, len(current)):
		#Mira quien es el padre del estado c
		index = trie.get_parent(c)
		#Lo que me cuesta 
		current[c] = current[index] + 1

	for letter in x:
		previous, current = current, previous
		current[0] = previous[0] + 1
		for st in range(trie.get_num_states()):
			parent = trie.get_parent(st)
			current[st] = min(current[parent] + 1,
							previous[st] + 1,
							previous[parent] + (letter != trie.get_label(st))
			)
		if min(current) > th:
			return {}
	
	aux = {trie.get_output(st):current[st] for st in range(trie.get_num_states()) if trie.is_final(st) and current[st] <= th}

	return list(aux.items())

def dp_restricted_damerau_trie(x, trie, th):
    # TODO
    return []

def dp_intermediate_damerau_trie(x, trie, th):
    # TODO
    return []


words = ["algortimo", "algortximo","lagortimo", "agaloritom", "algormio", "ba"]
words.sort()
trie = Trie(words)

test = ["algoritmo", "acb"]
thrs = range(1, 4)

for threshold in thrs:
    print(f"threshols: {threshold:3}")
    for x in test:
        for dist,name in (
                    (dp_levenshtein_trie,"levenshtein"),
                    (dp_restricted_damerau_trie,"restricted"),
                    (dp_intermediate_damerau_trie,"intermediate"),
                    ):
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
	algoritmo    	intermediate	[('algormio', 2), ('algortimo', 1), ('lagortimo', 2), ('agaloritom', 3), ('algortximo', 2)]
	acb          	levenshtein	[('ba', 3)]
	acb          	restricted	[('ba', 3)]
	acb          	intermediate	[('ba', 2)]

"""         
