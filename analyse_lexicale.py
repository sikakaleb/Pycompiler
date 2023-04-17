import sys
from sly import Lexer

import sys
from sly import Lexer


class FloLexer(Lexer):
    tokens = {
        IDENTIFIANT,
        ENTIER,
        ENT,
        ECRIRE,
        INFERIEUR_OU_EGAL,
        # TANTQUE,
        BOOLEEN,
        # SI,
        # ALORS,
        # SINON,
        # ET,
        # OU,
        # NON,
        PLUS,
        MINUS,
        MULT,
        DIV
    }

    literals = {'+', '*', '-', '/', '%', '!',
                '[', ']', '{', '}', '(', ')', ',', ";", "=", '<', '>', '&'}

    # ET = r'et'
    # OU = r'ou'
    # NON = r'non'
    PLUS = r'\+'
    MINUS = r'-'
    MULT = r'\*'
    DIV = r'/'

    ignore = ' \t'

    INFERIEUR_OU_EGAL = r'<='

    @_(r'0|[1-9][0-9]*')
    def ENTIER(self, t):
        t.value = int(t.value)
        return t

    IDENTIFIANT = r'[a-zA-Z][a-zA-Z0-9_]*'

    IDENTIFIANT['entier'] = ENT
    IDENTIFIANT['booleen'] = BOOLEEN
    IDENTIFIANT['ecrire'] = ECRIRE
    # IDENTIFIANT['si'] = SI
    # IDENTIFIANT['alors'] = ALORS
    # IDENTIFIANT['sinon'] = SINON
    # IDENTIFIANT['tantque'] = TANTQUE

    ignore_comment = r'\#.*'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f'Ligne {self.lineno}: caractère inattendu "{t.value[0]}"')
        self.index += 1


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python3 analyse_lexicale.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1], "r") as f:
            data = f.read()
            lexer = FloLexer()
            for tok in lexer.tokenize(data):
                print(tok)
