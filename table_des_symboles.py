class TableSymboles:
    def __init__(self):
        self.symboles = {}

    def ajouter_fonction(self, nom, type_retour):
        self.symboles[nom] = type_retour
    def verifier_exist(self,nom):
        if nom in self.symboles:
            return True
        else:
            return False

    def verifier_type_retour(self, nom, type_retour):
        if nom in self.symboles and self.symboles[nom].type == type_retour:
            return True
        else:
            return False
