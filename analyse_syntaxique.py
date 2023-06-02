import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait


class FloParser(Parser):
    tokens = FloLexer.tokens
    debugfile = "parser.out"

    precedence = (
        ('nonassoc', 'COMPARATEUR', 'INF', 'SUP',
         'INF_EGAL', 'SUP_EGAL', 'EGAL', 'DIFF'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'MULT', 'DIV'),
        ('nonassoc', 'UMINUS'),
        ('left', 'ET'),
        ('left', 'OU'),
        ('nonassoc', 'NON'),
    )

    @_('prog')
    def statement(self, p):
        return p.prog

    @_('listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p.listeInstructions)

    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        # l.instructions.insert(0,p.instruction)
        l.append(p.instruction)
        return l

    @_('listeInstructions instruction')
    def listeInstructions(self, p):
        # p.listeInstructions.instructions.insert(0,p.instruction)
        p.listeInstructions.append(p.instruction)
        return p.listeInstructions

    # 'structure_iteration')
    @_('ecrire', 'declaration', 'affectation', 'structure_conditionnelle', 'boucle')
    def instruction(self, p):
        return p[0]

    @_('ECRIRE "(" expr ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expr)

    @_('ENT IDENTIFIANT "=" expr ";"')
    def declaration(self, p):
        return arbre_abstrait.Declaration(p.IDENTIFIANT, p.expr, "ENTIER")

    @_('BOOLEEN IDENTIFIANT "=" expr ";"')
    def declaration(self, p):
        return arbre_abstrait.Declaration(p.IDENTIFIANT, p.expr, "BOOLEEN")

    @_('IDENTIFIANT "=" expr ";"')
    def affectation(self, p):
        return arbre_abstrait.Affectation(p.IDENTIFIANT, p.expr)
    #

    @_('SI expr ALORS "{" listeInstructions "}"  SINON  "{" listeInstructions "}"  ')
    def structure_conditionnelle(self, p):
        return arbre_abstrait.Condition(p.expr, p.listeInstructions0, p.listeInstructions1)

    @_('TANTQUE expr "{" listeInstructions "}"')
    def boucle(self, p):
        return arbre_abstrait.TantQue(p.expr, p.listeInstructions)

    # @_('REPETER "{" listeInstructions "}" JUSQU_A expr ";"')
    # def structure_iteration(self, p):
    #    return arbre_abstrait.Repeter(p.listeInstructions, p.expr)

    @_('expr PLUS term',
       'expr MINUS term',
       'expr ET expr',
       'expr OU expr')
    def expr(self, p):
        return arbre_abstrait.Operation(p[1], p[0], p[2])

    @_('expr INF expr',
       'expr SUP expr',
       'expr COMPARATEUR expr',
       # 'expr SUP_EGAL expr',
       'expr EGAL expr',
       'expr DIFF expr')
    def expr(self, p):
        return arbre_abstrait.Operation(p[1], p[0], p[2])

    @_('term')
    def expr(self, p):
        return p.term

    @_('term MULT factor',
       'term DIV factor')
    def term(self, p):
        return arbre_abstrait.Operation(p[1], p.term, p.factor)

    @_('factor')
    def term(self, p):
        return p.factor

    @_('ENTIER')
    def factor(self, p):
        return arbre_abstrait.Entier(p.ENTIER)

    @_('IDENTIFIANT')
    def factor(self, p):
        return arbre_abstrait.Identifiant(p.IDENTIFIANT)

    @_(' "(" expr ")" ')
    def factor(self, p):
        return p.expr

    @_('BOOLEEN')
    def factor(self, p):
        return arbre_abstrait.Booleen(p.BOOLEEN)

    @_('BOOLEEN_LITERAL')
    def factor(self, p):
        return arbre_abstrait.Booleen(p.BOOLEEN_LITERAL)

    @_('NON BOOLEEN_LITERAL')
    def expr(self, p):
        return arbre_abstrait.Operation("non", arbre_abstrait.Booleen(p.BOOLEEN_LITERAL), None)

    @_('NON IDENTIFIANT')
    def expr(self, p):
        return arbre_abstrait.Operation("non", arbre_abstrait.Identifiant(p.IDENTIFIANT), None)

    @_('MINUS expr %prec UMINUS')
    def expr(self, p):
        return arbre_abstrait.Operation('-', p.expr)


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
