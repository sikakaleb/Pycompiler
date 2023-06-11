"""
Affiche une chaine de caractère avec une certaine identation
"""


def afficher(s, indent=0):
    print(" "*indent+s)


class Programme:
    def __init__(self, listeInstructions):
        self.listeInstructions = listeInstructions

    def afficher(self, indent=0):
        afficher("<programme>", indent)
        self.listeInstructions.afficher(indent+1)
        afficher("</programme>", indent)


class ListeInstructions(list):
    def __init__(self):
        pass

    def afficher(self, indent=0):
        afficher("<listeInstructions>", indent)
        for instruction in self:
            if instruction is not None:
                instruction.afficher(indent+1)
        afficher("</listeInstructions>", indent)


class Ecrire:
    def __init__(self, exp):
        self.exp = exp

    def afficher(self, indent=0):
        afficher("<ecrire>", indent)
        self.exp.afficher(indent+1)
        afficher("</ecrire>", indent)


class Lire:
    def __init__(self, exp=None):
        self.exp = exp

    def afficher(self, indent=0):
        afficher("[lire:]", indent)


class Operation:
    def __init__(self, op, exp1, exp2=None):
        self.exp1 = exp1
        self.op = op
        self.exp2 = exp2

    def afficher(self, indent=0):
        afficher("<operation>", indent)
        afficher(self.op, indent+1)
        self.exp1.afficher(indent+1)
        if self.exp2 is not None:
            self.exp2.afficher(indent+1)
        afficher("</operation>", indent)


class Entier:
    def __init__(self, valeur):
        self.valeur = valeur

    def afficher(self, indent=0):
        afficher("[Entier:"+str(self.valeur)+"]", indent)


class Booleen:
    def __init__(self, valeur):
        self.valeur = valeur

    def afficher(self, indent=0):
        if (self.valeur == True):
            afficher(f"[Booleen:vrai]", indent)
        elif (self.valeur == False):
            afficher(f"[Booleen:faux]", indent)
        else:
            afficher("[Booleen:"+str(self.valeur)+"]", indent)


class Declaration:
    def __init__(self, identifiant, expression, type):
        self.identifiant = identifiant
        self.expression = expression
        self.type = type

    def afficher(self, indent=0):
        afficher("<declaration>", indent)
        afficher(f"[Identifiant: {self.identifiant}]", indent + 1)
        afficher(f"[Type: {self.type}]", indent + 1)
        self.expression.afficher(indent + 1)
        afficher("</declaration>", indent)


class Affectation:
    def __init__(self, identifiant, expression):
        self.identifiant = identifiant
        self.expression = expression

    def afficher(self, indent=0):
        afficher("<affectation>", indent)
        afficher(f"[Identifiant: {self.identifiant}]", indent + 1)
        self.expression.afficher(indent + 1)
        afficher("</affectation>", indent)


class Condition:
    def __init__(self, expression, liste_instructions_vrai, suite_sinosi):
        self.expression = expression
        self.liste_instructions_vrai = liste_instructions_vrai
        self.suite_sinosi = suite_sinosi

    def afficher(self, indent=0):
        afficher("<condition>", indent)
        if self.expression:
            self.expression.afficher(indent + 1)
        afficher("<alors>", indent)
        self.liste_instructions_vrai.afficher(indent + 1)
        afficher("</alors>", indent)
        if self.suite_sinosi:
            if isinstance(self.suite_sinosi, Condition):
                afficher("<sinon>", indent)
                self.suite_sinosi.afficher(indent + 1)
                afficher("</sinon>", indent)
            else:
                afficher("<sinon>", indent)
                self.suite_sinosi.afficher(indent + 1)
                afficher("</sinon>", indent)
        afficher("</condition>", indent)


class Identifiant:
    def __init__(self, nom):
        self.nom = nom

    def afficher(self, indent=0):
        afficher(f"[Identifiant:{self.nom}]", indent)


class TantQue:
    def __init__(self, expression, liste_instructions):
        self.expression = expression
        self.liste_instructions = liste_instructions

    def afficher(self, indent=0):
        afficher("<tantque>", indent)
        self.expression.afficher(indent + 1)
        self.liste_instructions.afficher(indent + 1)
        afficher("</tantque>", indent)

# dans l'arbre abstrait


class Fonction:
    def __init__(self, identifiant, type, param_list, liste_instructions):
        self.identifiant = identifiant
        self.type = type
        self.param_list = param_list
        self.liste_instructions = liste_instructions

    def afficher(self, indent=0):
        afficher("<fonction>", indent)
        afficher(f"[Identifiant: {self.identifiant}]", indent + 1)
        afficher(f"[Type: {self.type}]", indent + 1)
        if self.param_list:
            afficher("<parametres>", indent + 1)
            for param in self.param_list:
                param.afficher(indent + 2)
            afficher("</parametres>", indent + 1)
        self.liste_instructions.afficher(indent + 1)
        afficher("</fonction>", indent)


class AppelFonction:
    def __init__(self, identifiant, args):
        self.identifiant = identifiant
        self.args = args

    def afficher(self, indent=0):
        afficher("<appelFonction>", indent)
        afficher(f"[Identifiant: {self.identifiant}]", indent + 1)
        if self.args:
            afficher("<arguments>", indent + 1)
            for arg in self.args:
                arg.afficher(indent + 2)
            afficher("</arguments>", indent + 1)
        afficher("</appelFonction>", indent)


class Retourner:
    def __init__(self, expression):
        self.expression = expression

    def afficher(self, indent=0):
        afficher("<retourner>", indent)
        self.expression.afficher(indent + 1)
        afficher("</retourner>", indent)


class Parametre:
    def __init__(self, type, identifiant):
        self.type = type
        self.identifiant = identifiant

    def afficher(self, indent=0):
        afficher("<parametre>", indent)
        afficher(f"[Identifiant: {self.identifiant}]", indent + 1)
        afficher(f"[Type: {self.type}]", indent + 1)
        afficher("</parametre>", indent)
