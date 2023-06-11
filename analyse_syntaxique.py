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

    @_('listeFonctions')
    def prog(self, p):
        return arbre_abstrait.Programme(p.listeFonctions)

    @_('listeFonctions listeInstructions')
    def prog(self, p):
        return arbre_abstrait.Programme(p.listeFonctions, p.listeInstructions)

    @_('fonction_declaration_without_parm')
    def listeFonctions(self, p):
        l = arbre_abstrait.ListeFonctions()
        l.append(p.fonction_declaration_without_parm)
        return l

    @_('fonction_declaration')
    def listeFonctions(self, p):
        l = arbre_abstrait.ListeFonctions()
        l.append(p.fonction_declaration)
        return l

    @_('listeFonctions fonction_declaration')
    def listeFonctions(self, p):
        p.listeFonctions.append(p.fonction_declaration)
        return p.listeFonctions

    @_('listeFonctions fonction_declaration_without_parm')
    def listeFonctions(self, p):
        p.listeFonctions.append(p.fonction_declaration_without_parm)
        return p.listeFonctions

    @_('listeInstructions instruction')
    def listeInstructions(self, p):
        p.listeInstructions.append(p.instruction)
        return p.listeInstructions

    @_('instruction')
    def listeInstructions(self, p):
        l = arbre_abstrait.ListeInstructions()
        l.append(p.instruction)
        return l

    @_('ecrire', 'declaration', 'affectation', 'condition', 'boucle', 'retourner', 'appel_fonction_instr', 'appel_fonction_instr_without_parm')
    def instruction(self, p):
        return p[0]

    # @_("fonction_declaration_without_parm", "fonction_declaration")
    # def instruction(self, p):
    #    return p[0]

    @_('ECRIRE "(" expr ")" ";"')
    def ecrire(self, p):
        return arbre_abstrait.Ecrire(p.expr)

    @_('type IDENTIFIANT "=" expr ";"')
    def declaration(self, p):
        return arbre_abstrait.Declaration(p.IDENTIFIANT, p.expr, p.type)

    @_('type IDENTIFIANT ";"')
    def declaration(self, p):
        return arbre_abstrait.Declaration(p.IDENTIFIANT, None, p.type)

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

    @_('IDENTIFIANT "(" arg_list ")" ";" ')
    def appel_fonction_instr(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT, p.arg_list)

    @_("IDENTIFIANT '(' arg_list ')'")
    def appel_fonction_expr(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT, p.arg_list)

    @_('IDENTIFIANT "(" ")" ";"')
    def appel_fonction_instr_without_parm(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT, [])

    @_('IDENTIFIANT "(" ")" ')
    def appel_fonction_expr_without_parm(self, p):
        return arbre_abstrait.AppelFonction(p.IDENTIFIANT, [])

    @_('type IDENTIFIANT "(" param_list ")" "{" listeInstructions "}"')
    def fonction_declaration(self, p):
        return arbre_abstrait.Fonction(p.IDENTIFIANT, p.type, p.param_list, p.listeInstructions)

    @_("type IDENTIFIANT '(' ')' '{' listeInstructions '}'")
    def fonction_declaration_without_parm(self, p):
        return arbre_abstrait.Fonction(p.IDENTIFIANT, p.type, [], p.listeInstructions)

    @_("param")
    def param_list(self, p):
        return [p.param]

    @_("param_list ',' param")
    def param_list(self, p):
        p.param_list.append(p.param)
        return p.param_list

    @_("type IDENTIFIANT")
    def param(self, p):
        return arbre_abstrait.Parametre(p.type, p.IDENTIFIANT)

    @_('term PLUS expr')
    def expr(self, p):
        return arbre_abstrait.Operation(p.PLUS, p.term, p.expr)

    @_('term MINUS expr')
    def expr(self, p):
        return arbre_abstrait.Operation(p.MINUS, p.term, p.expr)

    @_("term")
    def expr(self, p):
        return p.term

    @_('expr MODULO term')
    def expr(self, p):
        return arbre_abstrait.Operation(p[1], p[0], p[2])

    @_('expr COMPARATEUR expr',)
    def expr(self, p):
        return arbre_abstrait.Operation(p[1], p[0], p[2])

    @_("term MULT factor")
    def term(self, p):
        return arbre_abstrait.Operation(p.MULT, p.term, p.factor)

    @_("term DIV factor")
    def term(self, p):
        return arbre_abstrait.Operation(p.DIV, p.term, p.factor)

    @_("factor")
    def term(self, p):
        return p.factor

    @_('appel_fonction_expr')
    def factor(self, p):
        return p.appel_fonction_expr

    @_('appel_fonction_expr_without_parm')
    def factor(self, p):
        return p.appel_fonction_expr_without_parm

    @_('ENTIER')
    def factor(self, p):
        return arbre_abstrait.Entier(p.ENTIER)

    @_('BOOLEEN_LITERAL')
    def factor(self, p):
        return arbre_abstrait.Booleen(p.BOOLEEN_LITERAL)

    @_("'(' expr ')'")
    def factor(self, p):
        return p.expr

    @_('IDENTIFIANT')
    def factor(self, p):
        return arbre_abstrait.Identifiant(p.IDENTIFIANT)

    @_('expr ET expr')
    def expr(self, p):
        return arbre_abstrait.Operation(p.ET, p[0], p[2])

    @_('factor OU expr')
    def factor(self, p):
        return arbre_abstrait.Operation(p.OU, p.factor, p.expr)

    @_('NON expr')
    def factor(self, p):
        return arbre_abstrait.Operation("non", p.expr, None)

    @_("MINUS factor %prec UMINUS")
    def factor(self, p):
        return arbre_abstrait.Operation('*', arbre_abstrait.Entier(-1), p.factor)

    @_('LIRE "(" ")"')
    def factor(self, p):
        return arbre_abstrait.Lire()

    @_('BOOLEEN')
    def type(self, p):
        return p.BOOLEEN

    @_('ENT')
    def type(self, p):
        return p.ENT

    @_("expr")
    def arg_list(self, p):
        return [p.expr]

    @_("arg_list ',' expr")
    def arg_list(self, p):
        p.arg_list.append(p.expr)
        return p.arg_list


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
