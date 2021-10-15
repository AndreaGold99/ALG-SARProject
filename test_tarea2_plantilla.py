#!/usr/bin/env python3
# Elias Urios Alacreu
# Andrea Cerverón Carot
# Jose María Valverde García 


""" ALL FUNCTIONS ARE A SMALL VARIATON FROM PART1, JUST CHECK IF STATEMENTS"""
import pdb

def dp_levenshtein_threshold(x, y, th):
    """Same as the function on test_1, but checks min value with threshold"""
    currentrow = [0]*(1+len(x))
    previousrow = [0]*(1+len(x))
    currentrow[0] = 0

    for i in range(1, len(x) + 1):
        currentrow[i] = currentrow[i-1] + 1
    for j in range(1, len(y) + 1):
        previousrow, currentrow = currentrow, previousrow
        currentrow[0] = previousrow[0] + 1
        for i in range(1, len(x) + 1):
            currentrow[i] = min(currentrow[i-1] + 1,
                previousrow[i] + 1,
                previousrow[i-1] + (x[i-1] != y[j-1]))
        #Threshold of currentrow
        if min(currentrow) > th:
            return th + 1
    #Return min between current and th + 1
    return min(currentrow[len(x)], th + 1)

def dp_restricted_damerau_threshold(x, y, th):  
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
        if min(currentrow) > th:
            return th + 1
    return min(currentrow[len(x)], th + 1)

def dp_intermediate_damerau_threshold(x, y, th):
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
    if min(currentrow) > th:
        return th + 1
    return min(currentrow[len(x)], th + 1)

test = [
        ("algoritmo","algortimo"),
        ("algoritmo","algortximo"),
        ("algoritmo","lagortimo"),
        ("algoritmo","agaloritom"),
        ("algoritmo","algormio"),
        ("acb","ba")
        ]

thrs = range(1,4)

if __name__=="__main__":
    for threshold in thrs:
        print(f"thresholds: {threshold:3}")
        for x,y in test:
            print(f"{x:12} {y:12} \t",end="")
            for dist,name in ((dp_levenshtein_threshold,"levenshtein"),
                            (dp_restricted_damerau_threshold,"restricted"),
                            (dp_intermediate_damerau_threshold,"intermediate")):

                print(f" {name} {dist(x,y,threshold):2}",end="")
            print()
                 
"""
Salida del programa:

thresholds:   1
algoritmo    algortimo    	 levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   	 levenshtein  2 restricted  2 intermediate  2
algoritmo    lagortimo    	 levenshtein  2 restricted  2 intermediate  2
algoritmo    agaloritom   	 levenshtein  2 restricted  2 intermediate  2
algoritmo    algormio     	 levenshtein  2 restricted  2 intermediate  2
acb          ba           	 levenshtein  3 restricted  2 intermediate  2
thresholds:   2
algoritmo    algortimo    	 levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   	 levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    	 levenshtein  3 restricted  2 intermediate  2
algoritmo    agaloritom   	 levenshtein  3 restricted  3 intermediate  3
algoritmo    algormio     	 levenshtein  3 restricted  3 intermediate  2
acb          ba           	 levenshtein  3 restricted  3 intermediate  2
thresholds:   3
algoritmo    algortimo    	 levenshtein  2 restricted  1 intermediate  1
algoritmo    algortximo   	 levenshtein  3 restricted  3 intermediate  2
algoritmo    lagortimo    	 levenshtein  4 restricted  2 intermediate  2
algoritmo    agaloritom   	 levenshtein  4 restricted  4 intermediate  3
algoritmo    algormio     	 levenshtein  3 restricted  3 intermediate  2
acb          ba           	 levenshtein  3 restricted  3 intermediate  2
"""         
