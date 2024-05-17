import sys
from sly import Lexer


class FloLexer(Lexer):
    tokens = {
        BOOLEEN_LITERAL,
        IDENTIFIANT,
        ENTIER,
        ENT,
        ECRIRE,
        TANTQUE,
        SI,
        ALORS,
        SINON,
        ET,
        OU,
        NON,
        PLUS,
        MINUS,
        MULT,
        DIV,
        UMINUS,
        BOOLEEN,
        COMPARATEUR,
        MODULO,
        LIRE,
        RETOURNER
    }


    BOOLEEN = r'booleen'
    ECRIRE = r'ecrire'
    LIRE = r'lire'
    SINON = r'sinon'
    SI = r'si'
    ALORS = r'alors'
    TANTQUE = r'tantque'
    RETOURNER = r'retourner'

    literals = {'+', '-', '*', '/', '(', ')', ';', '{', '}',
                '[', ']', ',',  '=', '<', '>', '&', '!', ':', '%'}

    @_(r'Vrai|Faux|booleen')
    def BOOLEEN_LITERAL(self, t):
        # Convertir la valeur en un vrai booléen
        if (t.value == 'booleen'):
            return t
        t.value = (t.value == 'Vrai')
        return t

    ET = r'et'
    OU = r'ou'
    NON = r'non'
    PLUS = r'\+'
    MINUS = r'-'
    MULT = r'\*'
    DIV = r'/'
    ignore = ' \t'
    UMINUS = r'-'
    ignore_comment = r'\#.*'

    @_('%')
    def MODULO(self, t):
        return t

    @_(r'<=|>=|<|>|==|!=')
    def COMPARATEUR(self, t):
        return t

    # INF = r'<'
    # SUP = r'>'
    # INF_EGAL = r'<='
    # SUP_EGAL = r'>='
    # EGAL = r'=='
    # DIFF = r'!='

    @_(r'0|[1-9][0-9]*')
    def ENTIER(self, t):
        t.value = int(t.value)
        return t

    IDENTIFIANT = r'(?!entier\b|booleen\b)[a-zA-Z][a-zA-Z0-9_]*'
    ENT = r'entier'

    @_(r'\n+')
    def ignore_newline(self, t):
        self.lineno += t.value.count('\n')

    def error(self, t):
        print(f"Ligne {self.lineno}: Caractère inattendu '{t.value[0]}'")
        self.index += 1

def index_tokens(lexer, text):
    index = 0
    for token in lexer.tokenize(text):
        # Récupérer la valeur du token sous forme de chaîne
        value = str(token.value)
        
        # Trouver la position de début de ce token dans le texte
        start = text.find(value, index)
        
        # Mettre à jour les attributs 'index' et 'end' du token
        token.index = start
        token.end = start + len(value)
        
        # Mettre à jour l'index pour la prochaine recherche
        index = token.end
        
        yield token

# Modifiez la section de code où vous appelez 'lexer.tokenize'
if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("usage: python3 analyse_lexicale.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1], "r") as f:
            data = f.read()
            lexer = FloLexer()
            for tok in index_tokens(lexer, data):
                print(tok)
