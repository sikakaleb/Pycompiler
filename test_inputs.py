import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch

from analyse_lexicale import FloLexer
from analyse_syntaxique import FloParser


class TestFloPrograms(unittest.TestCase):
    def setUp(self):
        self.maxDiff = None
        self.chemin_inputs = "input"
        self.lexer = FloLexer()
        self.parser = FloParser()

    def test_programs(self):
        for nom_fichier in os.listdir(self.chemin_inputs):
            print(nom_fichier)
            if nom_fichier == 'eval_lexical.flo':
                continue
            with self.subTest(nom_fichier=nom_fichier):
                # Chargement du fichier
                chemin_fichier = os.path.join(self.chemin_inputs, nom_fichier)
                with open(chemin_fichier, 'r') as f:
                    code = f.read()

                # Analyse lexicale et syntaxique du code
                with patch('sys.stdout', new=StringIO()) as fake_out:
                    self.parser.parse(self.lexer.tokenize(code))
                    arbre_syntaxique = fake_out.getvalue().strip()

                # Chargement du fichier contenant l'arbre attendu
                chemin_arbre = os.path.join(
                    "arbre_attendu", f"{nom_fichier}.txt")
                with open(chemin_arbre, 'r') as f:
                    arbre_attendu = f.read().strip()

                # Comparaison de l'arbre obtenu avec l'arbre attendu
                self.assertEqual(arbre_syntaxique, arbre_attendu)


if __name__ == '__main__':
    unittest.main(argv=sys.argv)
