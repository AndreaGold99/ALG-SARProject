# -*- coding: utf-8 -*-
import re
from test_tarea2_plantilla import (
    dp_intermediate_damerau_threshold,
    dp_levenshtein_threshold,
    dp_restricted_damerau_threshold,
    dp_levenshtein_threshold_optimistic,
)
import numpy as np
from trie import Trie
from test_tarea4_plantilla import dp_levenshtein_trie


class SpellSuggester:

    """
    Clase que implementa el método suggest para la búsqueda de términos.
    """

    def __init__(self, vocab_file_path):
        """Método constructor de la clase SpellSuggester

        Construye una lista de términos únicos (vocabulario),
        que además se utiliza para crear un trie.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.

        """
        # Hemos añadido un if para saber si es vocabulario o path
        if type(vocab_file_path) is str:
            self.vocabulary = self.build_vocab(
                vocab_file_path, tokenizer=re.compile("\W+")
            )
        else:
            self.vocabulary = vocab_file_path

    def pick_distance(self, distance):
        if distance == "levenshtein":
            return dp_levenshtein_threshold
        elif distance == "restricted":
            return dp_restricted_damerau_threshold
        elif distance == "optimistic":
            return dp_levenshtein_threshold_optimistic
        else:
            return dp_intermediate_damerau_threshold

    def build_vocab(self, vocab_file_path, tokenizer):
        """Método para crear el vocabulario.

        Se tokeniza por palabras el fichero de texto,
        se eliminan palabras duplicadas y se ordena
        lexicográficamente.

        Args:
            vocab_file (str): ruta del fichero de texto para cargar el vocabulario.
            tokenizer (re.Pattern): expresión regular para la tokenización.
        """
        with open(vocab_file_path, "r", encoding="utf-8") as fr:
            vocab = set(tokenizer.split(fr.read().lower()))
            vocab.discard("")  # por si acaso
            return sorted(vocab)

    def suggest(self, term, distance="levenshtein", threshold=0):

        """Método para sugerir palabras similares siguiendo la tarea 3.

        A completar.

        Args:
            term (str): término de búsqueda.
            distance (str): algoritmo de búsqueda a utilizar
                {"levenshtein", "restricted", "intermediate", "optimistic"}.
            threshold (int): threshold para limitar la búsqueda
                puede utilizarse con los algoritmos de distancia mejorada de la tarea 2
                o filtrando la salida de las distancias de la tarea 2
        """
        assert distance in ["levenshtein", "restricted", "intermediate", "optimistic"]

        results = {}  # diccionario termino:distancia
        dist_algo = self.pick_distance(distance)
        for voc in self.vocabulary:
            if abs(len(term) - len(voc)) <= threshold:
                dist = dist_algo(term, voc, threshold)
                if dist <= threshold:
                    results[voc] = dist
        return results


class TrieSpellSuggester(SpellSuggester):
    """
    Clase que implementa el método suggest para la búsqueda de términos y añade el trie
    """

    def __init__(self, vocab_file_path):
        super().__init__(vocab_file_path)
        self.trie = Trie(self.vocabulary)

    def suggest(self, term, threshold=0):
        results = dp_levenshtein_trie(term, self.trie, threshold)


if __name__ == "__main__":
    spellsuggester = SpellSuggester("./corpora/quijote.txt")
    print(spellsuggester.suggest("quixot", threshold=2))
    # cuidado, la salida es enorme print(suggester.trie)
