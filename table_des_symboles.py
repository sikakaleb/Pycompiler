class TableSymboles:
    types = {
        type(1): "entier",
        type(True): "booleen"
    }

    def __init__(self):
        self.symboles = {}

    def ajouter_fonction(self, nom, type_retour, arguments):
        self.symboles[nom] = {'type_retour': type_retour,
                              'args': arguments,
                              'memoire': len(arguments) * 4
                              }

    def verifier_exist(self, nom, type_args):
        if nom in self.symboles:
            if len(type_args) != len(self.symboles[nom]['args']):
                return False

            return [TableSymboles.types[i] for i in type_args] == self.symboles[nom]['args']
        else:
            return False

    def return_type(self, nom):
            return self.symboles[nom]['type_retour']

    def verifier_type_retour(self, nom, type_retour):
        if nom in self.symboles and self.symboles[nom]['type_retour'] == type_retour:
            return True
        else:
            return False
