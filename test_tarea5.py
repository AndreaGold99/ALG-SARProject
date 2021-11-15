import time
import collections
import re
import random
import math
import numpy as np
from spellsuggest import SpellSuggester, TrieSpellSuggester


def read_file(vocab_file_path="./corpora/quijote.txt"):
    tokenizer = re.compile("\W+")
    with open(vocab_file_path, "r", encoding="utf-8") as fr:
        c = collections.Counter(tokenizer.split(fr.read().lower()))
        if "" in c:
            del c[""]
        reversed_c = [(freq, word) for (word, freq) in c.items()]
        sorted_reversed = sorted(reversed_c, reverse=True)
        sorted_vocab = [word for (freq, word) in sorted_reversed]
        return sorted_vocab


def build_trie(vocab, n):
    return TrieSpellSuggester(sorted(vocab[:n]))


def build_suggest(vocab, n):
    s = SpellSuggester(vocab[:n])
    return s


def dummy_function(prepare_args=()):
    return "hello world"


def measure_time(function, arguments, prepare=dummy_function, prepare_args=()):

    # mide el tiempo de ejecutar function(*arguments)
    # IMPORTANTE: como se puede ejecutar varias veces puede que sea
    # necesario pasarle una función que establezca las condiciones
    # necesarias para medir adecuadamente (ej: si mides el tiempo de
    # ordenar algo y lo deja ordenado, la próxima vez que ordenes no
    # estará desordenado)
    # DEVUELVE: tiempo y el valor devuelto por la función
    # ESTA FUNCION SE IGNORA

    count, accum = 0, 0
    while accum < 0.1:
        prepare(*prepare_args)
        t_ini = time.process_time()
        returned_value = function(*arguments)
        accum += time.process_time() - t_ini
        count += 1
    return accum / count, returned_value


def check_times():
    vocab = read_file()
    print("TALLA\tDISTANCIA\tTHRESHOLD\tMEDIA\tMEDIANA\tDEV.TIPICA")
    print("-" * 6)
    # Distancias sin el trie
    for dist in ["levenshtein", "restricted", "intermediate", "optimistic"]:
        for talla in range(2500, len(vocab) // 2, 2000):
            # Creamos los vocabularios del suggest y del trie con un size talla
            suggest_vocab = build_suggest(vocab, talla)
            # 10 palabras aleatorias
            muestra = random.sample(suggest_vocab.vocabulary, 10)
            t1, t2 = 0, 0
            # Para cada threshold vamos a calcular tiempos sin importar el threshold
            for th in range(1, 6):
                tiempos = []
                for word in muestra:
                    t1 = time.process_time()
                    suggest_vocab.suggest(word, dist, th)
                    t2 = time.process_time() - t1
                    tiempos.append(t2)
                mn = round(np.mean(tiempos), 3)
                med = round(np.median(tiempos), 3)
                dev = round(np.std(tiempos), 3)
                print(f"{talla}\t{dist}\t{th}\t\t{mn}\t{med}\t{dev}")
            print("\n")
    for talla in range(2500, len(vocab) // 2, 2000):
        trie_vocab = build_trie(vocab, talla)
        muestra = random.sample(trie_vocab.vocabulary, 10)
        for th in range(1, 6):
            tiempos = []
            for word in muestra:
                t1 = time.process_time()
                trie_vocab.suggest(word, th)
                t2 = time.process_time() - t1
                tiempos.append(t2)
            mn = round(np.mean(tiempos), 3)
            med = round(np.median(tiempos), 3)
            dev = round(np.std(tiempos), 3)
            print(f"{talla}\tlevenshtein_trie\t{th}\t\t{mn}\t{med}\t{dev}")
        print("\n")
    print("#" * 64)


if __name__ == "__main__":
    check_times()
