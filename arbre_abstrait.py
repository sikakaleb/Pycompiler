"""
Affiche une chaine de caractère avec une certaine identation
"""
def afficher(s,indent=0):
	print(" "*indent+s)
	
class Programme:
	def __init__(self,listeInstructions):
		self.listeInstructions = listeInstructions
	def afficher(self,indent=0):
		afficher("<programme>",indent)
		self.listeInstructions.afficher(indent+1)
		afficher("</programme>",indent)

class ListeInstructions:
	def __init__(self):
		self.instructions = []
	def afficher(self,indent=0):
		afficher("<listeInstructions>",indent)
		for instruction in self.instructions:
			instruction.afficher(indent+1)
		afficher("</listeInstructions>",indent)
			
class Ecrire:
	def __init__(self,exp):
		self.exp = exp
	def afficher(self,indent=0):
		afficher("<ecrire>",indent)
		self.exp.afficher(indent+1)
		afficher("</ecrire>",indent)
		
class Operation:
	def __init__(self,op,exp1,exp2):
		self.exp1 = exp1
		self.op = op
		self.exp2 = exp2
	def afficher(self,indent=0):
		afficher("<operation>",indent)
		afficher(self.op,indent+1)
		self.exp1.afficher(indent+1)
		self.exp2.afficher(indent+1)
		afficher("</operation>",indent)
class Entier:
	def __init__(self,valeur):
		self.valeur = valeur
	def afficher(self,indent=0):
		afficher("[Entier:"+str(self.valeur)+"]",indent)
  
class Declaration:
    def __init__(self, identifiant, expression):
        self.identifiant = identifiant
        self.expression = expression

    def afficher(self, indent=0):
        afficher("<declaration>", indent)
        afficher(f"[Identifiant: {self.identifiant}]", indent + 1)
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
    def __init__(self, expression, liste_instructions_vrai, liste_instructions_faux):
        self.expression = expression
        self.liste_instructions_vrai = liste_instructions_vrai
        self.liste_instructions_faux = liste_instructions_faux

    def afficher(self, indent=0):
        afficher("<condition>", indent)
        self.expression.afficher(indent + 1)
        afficher("<alors>", indent)
        self.liste_instructions_vrai.afficher(indent + 1)
        afficher("</alors>", indent)
        afficher("<sinon>", indent)
        self.liste_instructions_faux.afficher(indent + 1)
        afficher("</sinon>", indent)
        afficher("</condition>", indent)

  
