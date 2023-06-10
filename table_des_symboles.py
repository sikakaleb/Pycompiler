class TableSymboles:
    def __init__(self):
        self.symboles = {}

    def ajouter_fonction(self, nom, type_retour):
        self.symboles[nom] = type_retour

    def verifier_type_retour(self, nom, type_retour):
        if nom in self.symboles and self.symboles[nom] == type_retour:
            return True
        else:
            return False
