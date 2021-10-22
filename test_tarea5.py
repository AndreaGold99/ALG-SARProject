import time
import collections
import re
from spellsuggest import SpellSuggester, TrieSpellSuggester
import trie

def read_file(vocab_file_path = "./corpora/quijote.txt"):
    tokenizer = re.compile("\W+")
    with open(vocab_file_path, "r", encoding='utf-8') as fr:
        c = collections.Counter(tokenizer.split(fr.read().lower()))
        if '' in c:
            del c['']
        reversed_c = [(freq, word) for (word,freq) in c.items()]
        sorted_reversed = sorted(reversed_c, reverse=True)
        sorted_vocab = [word for (freq,word) in sorted_reversed]
        return sorted_vocab

def build_trie (vocab, n):
    aux = vocab[:n+1]
    trie(sorted(aux))

def dummy_function(prepare_args=()):
    return "hello world"

def measure_time(function, arguments,
    prepare=dummy_function, prepare_args=()):

    # mide el tiempo de ejecutar function(*arguments)
    #IMPORTANTE: como se puede ejecutar varias veces puede que sea
    #necesario pasarle una función que establezca las condiciones
    #necesarias para medir adecuadamente (ej: si mides el tiempo de
    #ordenar algo y lo deja ordenado, la próxima vez que ordenes no
    #estará desordenado)
    #DEVUELVE: tiempo y el valor devuelto por la función 

    count, accum = 0, 0
    while accum < 0.1:
        prepare(*prepare_args)
        t_ini = time.process_time()
        returned_value = function(*arguments)
        accum += time.process_time()-t_ini
        count += 1
    return accum/count, returned_value