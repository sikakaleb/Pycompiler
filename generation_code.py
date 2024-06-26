import sys
from analyse_lexicale import FloLexer
from analyse_syntaxique import FloParser
import arbre_abstrait
from table_des_symboles import TableSymboles

# Permet de donner des noms différents à toutes les étiquettes (en les appelant e0, e1,e2,...)
num_etiquette_courante = -1
table_des_symboles = TableSymboles()
fonction_en_cours = ""


def nom_nouvelle_etiquette():
    global num_etiquette_courante
    num_etiquette_courante += 1
    return " e " + str(num_etiquette_courante)


afficher_table = False
afficher_nasm = False
"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""


def printifm(*args, **kwargs):
    if afficher_nasm:
        print(*args, **kwargs)


"""
Un print qui ne fonctionne que si la variable afficher_table vaut Vrai.
(permet de choisir si on affiche le code assembleur ou la table des symboles)
"""


def printift(*args, **kwargs):
    if afficher_table:
        print(*args, **kwargs)


"""
Fonction locale, permet d'afficher un commentaire dans le code nasm.
"""


def nasm_comment(comment):
    if comment != "":
        printifm(
            "\t\t ; " + comment)  # le point virgule indique le début d'un commentaire en nasm. Les tabulations sont là pour faire jolie.
    else:
        printifm("")


"""
Affiche une instruction nasm sur une ligne
Par convention, les derniers opérandes sont nuls si l'opération a moins de 3 arguments.
"""


def generer_code_comparaison():
    etiquette_vrai = nasm_nouvelle_etiquette()
    etiquette_fin = nasm_nouvelle_etiquette()

    nasm_instruction("cmp", "eax", "ebx", "", "")

    if operateur == "==":
        nasm_instruction("je", etiquette_vrai, "", "", "")
    elif operateur == "!=":
        nasm_instruction("jne", etiquette_vrai, "", "", "")
    elif operateur == "<":
        nasm_instruction("jl", etiquette_vrai, "", "", "")
    elif operateur == ">":
        nasm_instruction("jg", etiquette_vrai, "", "", "")
    elif operateur == "<=":
        nasm_instruction("jle", etiquette_vrai, "", "", "")
    elif operateur == ">=":
        nasm_instruction("jge", etiquette_vrai, "", "", "")

    nasm_instruction("push", "0", "", "", "")  # Mettre la valeur 0 sur la pile (faux)
    nasm_instruction("jmp", etiquette_fin, "", "", "")
    nasm_instruction(etiquette_vrai + ":")
    nasm_instruction("push", "1", "", "", "")  # Mettre la valeur 1 sur la pile (vrai)
    nasm_instruction(etiquette_fin + ":")


def nasm_instruction(opcode, op1="", op2="", op3="", comment=""):
    if op2 == "":
        printifm("\t" + opcode + "\t" + op1 + "\t\t", end="")
    elif op3 == "":
        printifm("\t" + opcode + "\t" + op1 + ",\t" + op2 + "\t", end="")
    else:
        printifm("\t" + opcode + "\t" + op1 +
                 ",\t" + op2 + ",\t" + op3, end="")
    nasm_comment(comment)


"""
Retourne le nom d'une nouvelle étiquette
"""

"""
Affiche le code nasm correspondant à tout un programme
"""


def gen_programme(programme):
    printifm('%include\t"io.asm"')
    printifm('section\t.bss')
    printifm(
        'sinput:	resb	255	;reserve a 255 byte space in memory for the users input string')
    printifm('v$a:	resd	1')
    printifm('section\t.text')
    printifm('global _start')
    gen_fonctions(programme.listeFonctions)
    printifm('_start:')
    gen_listeInstructions(programme.listeInstructions)
    # gen_listeInstructions(programme.listeInstructions)
    nasm_instruction("mov", "eax", "1", "", "1 est le code de SYS_EXIT")
    nasm_instruction("int", "0x80", "", "", "exit")


"""
Affiche le code nasm correspondant à une suite d'instructions
"""


def gen_fonctions(fonctions):
    for fonction in fonctions:
        if fonction.type == "entier" or fonction.type == "booleen":
            table_des_symboles.ajouter_fonction(fonction.identifiant, fonction.type,[parm.type for parm in fonction.param_list])
        else:
            print("your fonction don't return entier or booleen  ")
            exit(0)
    for fonction in fonctions:
        gen_def_fonction(fonction)


def gen_def_fonction(fonction):
    global fonction_en_cours
    printifm("_" + fonction.identifiant + ":")
    fonction_en_cours = fonction.identifiant
    gen_listeInstructions(fonction.liste_instructions)


def gen_listeInstructions(listeInstructions):
    for instruction in listeInstructions:
        gen_instruction(instruction)


"""
Affiche le code nasm correspondant à une instruction
"""


def gen_instruction(instruction):
    if type(instruction) == arbre_abstrait.Ecrire:
        gen_ecrire(instruction)
    elif type(instruction) == arbre_abstrait.Lire:
        gen_lire(instruction)
    elif type(instruction) == arbre_abstrait.TantQue:
        gen_tantque(instruction)
    elif type(instruction) == arbre_abstrait.Condition:
        gen_si(instruction)
    elif type(instruction) == arbre_abstrait.Retourner:
        gen_retourner(instruction)
    elif type(instruction) == arbre_abstrait.AppelFonction:
        gen_appel_fct(instruction)


    else:
        print("type instruction inconnu ", type(instruction))
        exit(0)


"""
Affiche le code nasm correspondant au fait d'envoyer la valeur entière d'une expression sur la sortie standard
"""


def gen_appel_fct(instruction):
    if table_des_symboles.verifier_exist(instruction.identifiant,[type(arg) for arg in instruction.args]):
        nasm_instruction("call", "_" + instruction.identifiant, "", "", "appel de la fonction")
        if table_des_symboles.return_type(instruction.identifiant)== "entier":
            return arbre_abstrait.Entier
        else:
            return arbre_abstrait.Booleen


def gen_retourner(retourner):
    global fonction_en_cours
    retour_fct = gen_expression(retourner.expression)
    if fonction_en_cours != "" and (
            (table_des_symboles.verifier_type_retour(fonction_en_cours,
                                                     "entier") and retour_fct == arbre_abstrait.Entier) or (
                    table_des_symboles.verifier_type_retour(fonction_en_cours,
                                                            "booleen") and retour_fct == arbre_abstrait.Booleen)):
        nasm_instruction("pop", "eax", "", "", "met le résultat dans eax")
        nasm_instruction("ret", "", "", "", "revenir à l’appel de la fonction")
        fonction_en_cours = ""
    else:
        print("Nous ne sommes pas dans une fonction ou type non concordant ", retour_fct)
        exit(0)


def gen_si(si):
    etiquette_vrai = nom_nouvelle_etiquette()
    etiquette_fin = nom_nouvelle_etiquette()
    type_exp = gen_expression(si.expression)
    if type_exp == arbre_abstrait.Booleen:
        nasm_instruction("pop", "eax", "", "", "mettre la valeur de la condition dans eax")
        nasm_instruction("cmp", "eax", "1", "", " vérifie si la condition est vraie")
        nasm_instruction("je", etiquette_vrai, "", "", "")
        gen_listeInstructions(si.liste_instructions_faux)
        nasm_instruction("jmp", etiquette_fin, "", "", "")
        nasm_instruction(etiquette_vrai)
        gen_listeInstructions(si.liste_instructions_vrai)
        nasm_instruction(etiquette_fin)
    else:
        print("you made a mistake ")
        exit(0)

    # return 2


def gen_tantque(tantque):
    etiquette_debut = nom_nouvelle_etiquette()
    etiquette_vrai = nom_nouvelle_etiquette()
    etiquette_fin = nom_nouvelle_etiquette()
    nasm_instruction(etiquette_debut)
    type_exp = gen_expression(tantque.expression)
    if type_exp == arbre_abstrait.Booleen:
        nasm_instruction("pop", "eax", "", "", "mettre la valeur de la condition dans eax")
        nasm_instruction("cmp", "eax", "1", "", " compare exp1 et exp2")
        nasm_instruction("je", etiquette_vrai, "", "", "")
        nasm_instruction("jmp", etiquette_fin, "", "", "")
        nasm_instruction(etiquette_vrai)
        gen_listeInstructions(tantque.liste_instructions)
        nasm_instruction("jmp", etiquette_debut, "", "", "")

        nasm_instruction(etiquette_fin)
    else:
        print("you made a mistake ")
        exit(0)

    # return 2


def gen_ecrire(ecrire):
    print(ecrire.exp)
    gen_expression(ecrire.exp)  # on calcule et empile la valeur d'expression
    # on dépile la valeur d'expression sur eax
    nasm_instruction("pop", "eax", "", "", "")
    # on envoie la valeur d'eax sur la sortie standard
    nasm_instruction("call", "iprintLF", "", "", "")


def gen_lire(ecrire):
    # charge l’adresse sinput dans eax
    nasm_instruction("mov", "eax", "sinput", "", "")
    # copie l’entrée utilisateur à l’adresse indiquée dans eax
    nasm_instruction("call", "readline", "", "", "")
    nasm_instruction("call", "atoi", "", "",
                     "")  # transforme la chaîne de caractère à l’adresse indiquée dans eax en entier et met le résultat dans eax
    nasm_instruction("push", "eax", "", "", "")  # empile eax.


"""
Affiche le code nasm pour calculer et empiler la valeur d'une expression
"""


def gen_expression(expression):
    if type(expression) == arbre_abstrait.Operation:
        return gen_operation(expression)
        # on calcule et empile la valeur de l'opération
    # if type(expression)==arbre_abstrait.Condition:
    #   gen_operation(expression)

    elif type(expression) == arbre_abstrait.Entier:
        nasm_instruction("push", str(expression.valeur), "", "", "")
        return arbre_abstrait.Entier  # on met sur la pile la valeur entière
    # elif (type(expression) == arbre_abstrait.Identifiant and (expression.nom == "vrai" or expression.nom == "faux"))or type(expression)==arbre_abstrait.Booleen:
    elif type(expression) == arbre_abstrait.Booleen:
        if str(expression.valeur) == "True":
            nasm_instruction("push", "1", "", "", "")
            return arbre_abstrait.Booleen  # on met sur la pile la valeur booléenne
        elif str(expression.valeur) == "False":
            nasm_instruction("push", "0", "", "", "")
            return arbre_abstrait.Booleen
    elif type(expression) == arbre_abstrait.AppelFonction:
        retour=gen_appel_fct(expression)
        nasm_instruction("push", "eax", "", "", "")
        return retour


    else:
        print("type d'expression inconnu", type(expression))
        exit(0)


"""
Affiche le code nasm pour calculer l'opération et la mettre en haut de la pile
"""


def gen_operation(operation):
    type_op = arbre_abstrait.Operation
    op = operation.op

    # on calcule et empile la valeur de exp1
    type_exp1 = gen_expression(operation.exp1)
    #print(type_exp1)
    # on calcule et empile la valeur de exp2
    if(op!="non"):
        type_exp2 = gen_expression(operation.exp2)
        nasm_instruction("pop", "ebx", "", "",
                     "dépile la seconde operande dans ebx")
    nasm_instruction("pop", "eax", "", "",
                     "dépile la permière operande dans eax")

    code = {"+": "add", "*": "imul", "-": "sub", "/": "idiv",
            "%": "modulo", "et": "and", "ou": "or",
            "non": "xor", "==": "je", "!=": "jne", "<": "jl", ">": "jg", "<=": "jle",
            ">=": "jge"}  # Un dictionnaire qui associe à chaque opérateur sa fonction nasm
    # Voir: https://www.bencode.net/blob/nasmcheatsheet.pdf
    if op in ['+']:
        nasm_instruction(code[op], "eax", "ebx", "",
                         "effectue l'opération eax" + op + "ebx et met le résultat dans eax")
    elif op == '*':
        nasm_instruction(code[op], "ebx", "", "", "effectue l'opération eax" +
                         op + "ebx et met le résultat dans eax")
    elif op == '-':
        nasm_instruction(code[op], "eax", "ebx", "",
                         "effectue l'opération eax" + op + "ebx et met le résultat dans eax")
    elif op == '/':
        nasm_instruction(code[op], "ebx", "", "",
                         "effectue l'opération eax" + op + "ebx et met le résultat dans eax")
    elif op == '%':
        nasm_instruction("idiv", "ebx", "", "",
                         "effectue l'opération eax" + op + "ebx et met le résultat dans eax")
        nasm_instruction("mov", "eax", "edx", "",
                         "effectue l'opération eax" + op + "ebx et met le résultat dans eax")
        # nasm_instruction(code[op], "ebx", "", "",
        # "effectue l'opération eax" + op + "ebx et met le résultat dans eax")
    elif op == 'et':
        if type_exp2 == arbre_abstrait.Booleen and type_exp1 == arbre_abstrait.Booleen:
            nasm_instruction(code[op], "eax", "ebx", "",
                             "effectue l'opération eax" + op + "ebx et met le résultat dans eax")
            type_op = arbre_abstrait.Booleen
        else:
            print("you made a mistake ")
            exit(0)
    elif op == 'ou':
        if type_exp2 == arbre_abstrait.Booleen and type_exp1 == arbre_abstrait.Booleen:
            nasm_instruction(code[op], "eax", "ebx", "",
                             "effectue l'opération eax" + op + "ebx et met le résultat dans eax")
            type_op = arbre_abstrait.Booleen
        else:
            print("you made a mistake ")
            exit(0)
    elif op == 'non':
        if type_exp1 == arbre_abstrait.Booleen:
            nasm_instruction(code[op], "eax", "1", "",
                             "effectue l'opération eax" + op + "ebx et met le résultat dans eax")
            type_op = arbre_abstrait.Booleen
        else:
            print("you made a mistake ")
            exit(0)


    elif op == "==" or op == "!=" or op == "<=" or op == ">=" or op == "<" or op == ">":
        etiquette_vrai = nom_nouvelle_etiquette()
        etiquette_fin = nom_nouvelle_etiquette()
        nasm_instruction("cmp", "eax", "ebx", "", " compare exp1 et exp2")
        nasm_instruction(code[op], etiquette_vrai, "", "", "")
        nasm_instruction("push", "0", "", "", "")  # Mettre la valeur 0 sur la pile (faux)
        nasm_instruction("jmp", etiquette_fin, "", "", "")
        nasm_instruction(etiquette_vrai)
        nasm_instruction("push", "1", "", "", "")  # Mettre la valeur 1 sur la pile (vrai)
        nasm_instruction(etiquette_fin)
        nasm_instruction("pop", "eax", "", "", "met le résultat dans eax")
        type_op = arbre_abstrait.Booleen
    nasm_instruction("push", "eax", "", "", "empile le résultat")
    return type_op


# ici je veux plutot faire une mv de 1 ou 0 dans eax


if __name__ == "__main__":
    afficher_nasm = True
    lexer = FloLexer()
    parser = FloParser()
    if len(sys.argv) < 3 or sys.argv[1] not in ["-nasm", "-table"]:
        print("usage: python3 generation_code.py -nasm|-table NOM_FICHIER_SOURCE.flo")
        exit(0)
    if sys.argv[1] == "-nasm":
        afficher_nasm = True
    else:
        afficher_tableSymboles = True
    with open(sys.argv[2], "r") as f:
        data = f.read()
        try:
            arbre = parser.parse(lexer.tokenize(data))
            gen_programme(arbre)
        except EOFError:
            exit()

# le ecrire(vrai) vrai est reconnu comme un identifiant à qméliorer
