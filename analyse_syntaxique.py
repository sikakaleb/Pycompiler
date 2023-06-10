import sys
from sly import Parser
from analyse_lexicale import FloLexer
import arbre_abstrait


class FloParser(Parser):
    tokens = FloLexer.tokens
    debugfile = "parser.out"

    precedence = (
        ('nonassoc', 'NON'),
        ('nonassoc', 'UMINUS'),
        ('left', 'MULT', 'DIV', 'MODULO'),
        ('left', 'PLUS', 'MINUS'),
        ('left', 'ET'),
        ('left', 'OU'),
        ('nonassoc', 'COMPARATEUR'),
    )

    @_('prog')
    def statement(self, p):
        return p.prog

    @_('listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p.listeInstructions)

    @_('listeInstructions instruction')
    def listeInstructions(self, p):
        # p.listeInstructions.instructions.insert(0,p.instruction)
        p.listeInstructions.append(p.instruction)
        return p.listeInstructions

    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        # l.instructions.insert(0,p.instruction)
        l.append(p.instruction)
        return l

    @_('ecrire', 'declaration', 'affectation', 'condition', 'boucle', 'retourner', 'appel_fonction_2', 'appel_fonction_1')
    def instruction(self, p):
        return p[0]

    @_("fonction_declaration")
    def instruction(self, p):
        return p.fonction_declaration

    @_('ECRIRE "(" expr ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expr)

    @_('type IDENTIFIANT "=" expr ";"')
    def declaration(self, p):
        return arbre_abstrait.Declaration(p.IDENTIFIANT, p.expr, p.type)

    @_('IDENTIFIANT "=" expr ";"')
    def affectation(self, p):
        return arbre_abstrait.Affectation(p.IDENTIFIANT, p.expr)

    @_('SI "(" expr ")" "{" listeInstructions "}" suite_sinosi')
    def condition(self, p):
        return arbre_abstrait.Condition(p.expr, p.listeInstructions, p.suite_sinosi)

    @_('SINON "{" listeInstructions "}"')
    def suite_sinosi(self, p):
        return p.listeInstructions

    @_('SINON SI "(" expr ")" "{" listeInstructions "}" suite_sinosi')
    def suite_sinosi(self, p):
        return arbre_abstrait.Condition(p.expr, p.listeInstructions, p.suite_sinosi)

    @_('')
    def suite_sinosi(self, p):
        return None

    @_('TANTQUE "(" expr ")" "{" listeInstructions "}"')
    def boucle(self, p):
        return arbre_abstrait.TantQue(p.expr, p.listeInstructions)

    @_('retourner')
    def retourner(self, p):
        return p.retourner

    @_('RETOURNER expr ";"')
    def retourner(self, p):
        return arbre_abstrait.Retourner(p.expr)

    @_('IDENTIFIANT "(" ")" ";"')
    def appel_fonction_2(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT)

    @_('IDENTIFIANT "(" ")" ')
    def appel_fonction_1(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT)

    @_("type IDENTIFIANT '(' ')' '{' listeInstructions '}'")
    def fonction_declaration(self, p):
        return arbre_abstrait.Fonction(p.IDENTIFIANT, p.type, p.listeInstructions)

    @_('ENTIER')
    def factor(self, p):
        return arbre_abstrait.Entier(p.ENTIER)

    @_('BOOLEEN_LITERAL')
    def factor(self, p):
        return arbre_abstrait.Booleen(p.BOOLEEN_LITERAL)

    @_(' "(" expr ")" ')
    def factor(self, p):
        return p.expr

    @_('IDENTIFIANT')
    def factor(self, p):
        return arbre_abstrait.Identifiant(p.IDENTIFIANT)

    @_('expr PLUS term')
    def expr(self, p):
        return arbre_abstrait.Operation(p.PLUS, p.expr, p.term)

    @_('expr MINUS term')
    def expr(self, p):
        return arbre_abstrait.Operation(p.MINUS, p.expr, p.term)

    @_('term')
    def expr(self, p):
        return p.term

    @_('appel_fonction_1')
    def term(self, p):
        return p.appel_fonction_1

    @_('term MULT factor')
    def term(self, p):
        return arbre_abstrait.Operation(p.MULT, p.term, p.factor)

    @_('term DIV factor')
    def term(self, p):
        return arbre_abstrait.Operation(p.DIV, p.term, p.factor)

    @_('term MODULO factor')
    def term(self, p):
        return arbre_abstrait.Operation(p[1], p[0], p[2])

    @_('factor')
    def term(self, p):
        return p.factor

    @_('factor ET expr')
    def factor(self, p):
        return arbre_abstrait.Operation(p.ET, p.factor, p.expr)

    @_('factor OU expr')
    def factor(self, p):
        return arbre_abstrait.Operation(p.OU, p.factor, p.expr)

    @_('NON expr')
    def factor(self, p):
        return arbre_abstrait.Operation("non", p.expr, None)

    @_('MINUS expr %prec UMINUS')
    def factor(self, p):
        return arbre_abstrait.Operation('*', p.expr, arbre_abstrait.Entier(-1))

    @_('expr COMPARATEUR expr',)
    def expr(self, p):
        return arbre_abstrait.Operation(p[1], p[0], p[2])

    @_('LIRE "(" ")"')
    def factor(self, p):
        return arbre_abstrait.Lire()

    @_('BOOLEEN')
    def type(self, p):
        return p.BOOLEEN

    @_('ENT')
    def type(self, p):
        return p.ENT
# Ajoutez des règles similaires pour les autres mots clés


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
