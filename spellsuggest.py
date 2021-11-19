# -*- coding: utf-8 -*-
from distancia_th import (
    dp_intermediate_damerau_threshold,
    dp_levenshtein_threshold,
    dp_restricted_damerau_threshold,
)
import numpy as np
from trie import Trie
from distancias_trie import dp_levenshtein_trie, dp_restricted_damerau_trie,  dp_intermediate_damerau_trie


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
        # Hemos añadido un if para saber si es vocabulario(lista) o path
        if type(vocab_file_path) is str:
            self.vocabulary = self.build_vocab(
                vocab_file_path, tokenizer=re.compile("\W+")
            )
        else:
            self.vocabulary = vocab_file_path

    def pick_distance(self, distance):
        """ Distancia a usar en funcion entre las diferentes"""
        if distance == "levenshtein":
            return dp_levenshtein_threshold
        elif distance == "restricted":
            return dp_restricted_damerau_threshold
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
        assert distance in ["levenshtein", "restricted", "intermediate"]

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
        self.trie = Trie(sorted(self.vocabulary))

    def suggest(self, term, distance, th=0):
        if distance == "levensthein":
            return dp_levenshtein_trie(term, self.trie, th)
        elif distance == "restricted":
            return dp_intermediate_damerau_trie(term, self.trie, th)
        else:
            return dp_restricted_damerau_trie(term, self.trie, th)
    


if __name__ == "__main__":
    spellsuggester = SpellSuggester("./corpora/quijote.txt")
    print(spellsuggester.suggest("quixot", threshold=2))
    # cuidado, la salida es enorme print(suggester.trie)
