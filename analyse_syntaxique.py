import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait


class FloParser(Parser):
    # On récupère la liste des lexèmes de l'analyse lexicale
    tokens = FloLexer.tokens

    # Règles gramaticales et actions associées

    @_('listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p[0])

    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        l.instructions.append(p[0])
        return l

    @_('instruction listeInstructions')
    def listeInstructions(self, p):
        p[1].instructions.append(p[0])
        return p[1]

    @_('ecrire', 'declaration', 'affectation', 'structure_conditionnelle')
    def instruction(self, p):
        return p[0]

    @_('ECRIRE "(" expr ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expr)

    @_('ENT IDENTIFIANT "=" expr ";"')
    def declaration(self, p):
        return arbre_abstrait.Declaration(p.IDENTIFIANT, p.expr)

    @_('IDENTIFIANT "=" expr ";"')
    def affectation(self, p):
        return arbre_abstrait.Affectation(p.IDENTIFIANT, p.expr)

    @_('SI expr ALORS "{" listeInstructions "}" SINON "{" listeInstructions "}"')
    def structure_conditionnelle(self, p):
        return arbre_abstrait.Condition(p.expr, p.listeInstructions0, p.listeInstructions1)

    @_('expr "+" expr')
    def expr(self, p):
        return arbre_abstrait.Operation('+', p[0], p[2])

    @_('expr "*" expr')
    def expr(self, p):
        return arbre_abstrait.Operation('*', p[0], p[2])

    @_('"(" expr ")"')
    def expr(self, p):
        return p.expr

    @_('ENTIER')
    def expr(self, p):
        return arbre_abstrait.Entier(p.ENTIER)
    


if __name__ == '__main__':
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 2:
        print("usage: python3 analyse_syntaxique.py NOM_FICHIER_SOURCE.flo")
    else:
        with open(sys.argv[1], "r") as f:
            data = f.read()
            try:
                arbre = parser.parse(lexer.tokenize(data))
                arbre.afficher()
            except EOFError:
                exit()
