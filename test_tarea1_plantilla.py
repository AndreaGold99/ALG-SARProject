import numpy as np

def dp_levenshtein_backwards(x, y):
    currentrow = [0]*(1+len(x))
    previousrow = [0]*(1+len(x))
    currentrow[0] = 0

    for i in range(1, len(x)+1):
        currentrow[i] = currentrow[i-1] + 1
    for j in range(1, len(y)+1):
        previousrow, currentrow = currentrow, previousrow
        currentrow[0] = previousrow[0] + 1
        for i in range(1, len(x)+1):
            currentrow[i] = min(currentrow[i-1] + 1,
                previousrow[i] + 1,
                previousrow[i-1]+(x[i-1] != y[j-1]))
    return currentrow[len(x)]

def dp_restricted_damerau_backwards(x, y):
    currentrow = [0]*(1+len(x))
    previousrow = [0]*(1+len(x))
    previousrow2 = [0]*(1+len(x))
    currentrow[0] = 0

    for i in range(1, len(x)+1):
        currentrow[i] = currentrow[i-1] + 1
    for j in range(1, len(y)+1):
        previousrow, currentrow, previousrow2 = currentrow, previousrow2, previousrow
        currentrow[0] = previousrow[0] + 1
        for i in range(1, len(x)+1):
            if i > 1 and j > 1 and x[i-2] == y[j-1] and x[i-1] == y[j-2]:
                aux = previousrow2[i-2] + 1
            else:
                aux = 10000
            currentrow[i] = min(currentrow[i-1] + 1,
                previousrow[i] + 1,
                previousrow[i-1]+(x[i-1] != y[j-1]),
                aux)
    return currentrow[len(x)]

def dp_intermediate_damerau_backwards(x, y):
    currentrow = [0]*(1+len(x))
    previousrow = [0]*(1+len(x))
    previousrow2 = [0]*(1+len(x))
    previousrow3 = [0]*(1+len(x))
    currentrow[0] = 0

    for i in range(1, len(x)+1):
        currentrow[i] = currentrow[i-1] + 1
    for j in range(1, len(y)+1):
        previousrow, currentrow, previousrow2, previousrow3 = currentrow, previousrow3, previousrow, previousrow2
        currentrow[0] = previousrow[0] + 1
        for i in range(1, len(x)+1):            
            currentrow[i] = min(currentrow[i-1] + 1,
                previousrow[i] + 1,
                previousrow[i-1]+(x[i-1] != y[j-1]))

            if i > 1 and j > 1 and x[i-2] == y[j-1] and x[i-1] == y[j-2]:
                currentrow[i] = min (currentrow[i], previousrow2[i-2] + 1)
            
            if i > 1 and j > 2 and x[i-2] == y[j-1] and x[i-1] == y[j-3]:
                currentrow[i] = min (currentrow[i], previousrow3[i-2] + 2)
                
            if i > 2 and j > 1 and x[i-3] == y[j-1] and x[i-1] == y[j-2]:
                currentrow[i] = min (currentrow[i], previousrow2[i-3] + 2)
    return currentrow[len(x)]

test = [("algoritmo","algortimo"),
        ("algoritmo","algortximo"),
        ("algoritmo","lagortimo"),
        ("algoritmo","agaloritom"),
        ("algoritmo","algormio"),
        ("acb","ba")]

for x,y in test:
    print(f"{x:12} {y:12}",end="")
    for dist,name in ((dp_levenshtein_backwards,"levenshtein"),
                      (dp_restricted_damerau_backwards,"restricted"),
                      (dp_intermediate_damerau_backwards,"intermediate")):
        print(f" {name} {dist(x,y):2}",end="")
    print()
                 
"""
Salida del programa:

algoritmo    algortimo    levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    levenshtein  4 restricted  2 intermediate  2
algoritmo    agaloritom   levenshtein  5 restricted  4 intermediate  3
algoritmo    algormio     levenshtein  3 restricted  3 intermediate  2
acb          ba           levenshtein  3 restricted  3 intermediate  2
"""         
