import subprocess
import os

total = 0
score = 0

def check(file_name,good_answer,lire=None):
	
	command = './output/'+file_name
	global total,score
	total+=1
	try:
		answer = subprocess.check_output([command],input=lire).decode()
	except Exception as e:
		print(file_name+": Erreur")
		print(e)
		return
		
	if answer == good_answer:
		print(file_name+": Ok")
		score+=1
	else:
		print(file_name+": Faux")
		print("Réponse attendu:")
		print(good_answer)
		print("Réponse étudiant:")
		print(answer)
		

def check_bad(file_name):
	global total,score
	total+=1
	if os.path.isfile('generation_code.py'): 
		command = ['python3', 'generation_code.py', '-nasm', 'bad_input/'+file_name+'.flo']
	elif os.path.isfile('main'): 
		command = ['main', '-n', 'bad_input/'+file_name+'.flo']
	else:
		print("Erreur: pas de fichier main ou generation_code.py. Vous êtes dans le bon dossier?")
		exit(1)
		
	try:
		subprocess.check_output(command)
		print(file_name+":Faux, ne devrait pas compiler et compile")
	except Exception as e:
		print(file_name+":Ok")
		score+=1

subprocess.check_output(['make'])
print('Dossier input:')
check("priorite",'14\n25\n19\n62\n15\n26\n29\n120\n');
check("arith_1",'13\n-13\n272\n92\n1011\n14901\n11804\n');
check("arith_2",'2738\n861952\n-156992\n0\n4092496\n');
check("arith_3",'607\n607\n2987\n1559\n3995\n1559\n');
check("arith_4",'-437\n-437\n1943\n1501\n-935\n1501\n85\n85\n3\n33\n1\n33\n85\n85\n2\n-25\n-7\n-25\n');
check("arith_5",'32810\n-32810\n-32810\n32810\n');
check("arith_6",'0\n12\n7\n');
check("lire",'1\n6\n9\n-1\n2\n4\n',b'1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n');
check("log",'0\n1\n1\n0\n0\n1\n1\n1\n0\n0\n0\n1\n0\n0\n1\n0\n0\n1\n0\n0\n1\n1\n1\n0\n');
check("comp",'1\n0\n0\n1\n1\n0\n0\n0\n1\n0\n1\n1\n1\n0\n1\n0\n1\n0\n1\n0\n1\n1\n');
check("boucle_1",'0\n0\n0\n1\n',b'1\n3\n7\n4\n');
check("boucle_2",'0\n2\n0\n2\n0\n1\n1\n2\n3\n',b'0\n2\n0\n3\n0\n1\n1\n2\n3');
check("si",'1\n2\n3\n4\n5\n6\n7\n8\n9\n10\n11\n12\n13\n14\n');
check("fonction_1",'3\n');
check("fonction_2",'6\n0\n');
check("fonction_3",'7\n');
check("fonction_4",'120\n');
check("fonction_5",'0\n-4\n5\n7\n');
check("fonction_6",'5\n');
check("fonction_7",'7\n');
check("fonction_8",'40\n');
check("fonction_9",'13\n');
check("fonction_10",'1\n1\n2\n3\n5\n8\n13\n21\n');
check("fonction_11",'3\n3\n3\n3\n3\n3\n');
check("fonction_12",'8\n81\n1024\n');
check("fonction_13",'1\n3\n6\n10\n15\n');
check("variable",'1\n3\n5\n7\n9\n12\n17\n22\n27\n32\n37\n42\n47\n52\n57\n62\n');
check("affectation",'12\n');
print('\nDossier bad_input:')
for i in range(1,6):
	check_bad('type_'+str(i))

check_bad('si')

for i in range(1,9):
	check_bad('fonction_'+str(i))
for i in range(1,7):
	check_bad('attribution_'+str(i))
print(f"\nscore:{score}/{total}")
