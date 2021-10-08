def dp_levenshtein_threshold(x, y, th):
    #TODO
    return 0

def dp_restricted_damerau_threshold(x, y, th):
    #TODO
    return 0

def dp_intermediate_damerau_threshold(x, y, th):
    #TODO
    return 0

test = [
        ("algoritmo","algortimo"),
        ("algoritmo","algortximo"),
        ("algoritmo","lagortimo"),
        ("algoritmo","agaloritom"),
        ("algoritmo","algormio"),
        ("acb","ba")
        ]

thrs = range(1,4)

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
acb          ba           	 levenshtein  2 restricted  2 intermediate  2
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
