import csv

def Insert_SQL(line):
	output.write("INSERT INTO Lieu ( nom_commune , code_dept , nom_dept , nom_region ) VALUES ("+str(line[dico['nom_commune']])+", "+str(line[dico['code_dept']])+", "+str(line[dico['nom_dept']])+", "+str(line[dico['nom_region']])+") ON CONFLICT (nom_commune) DO NOTHING;")
	output.write('\n')
	output.write("INSERT INTO Image ( nom_image , url , nom_monument , description , nom_commune , geoloc ) VALUES ('"+str(line[dico['nom_image']].split('/')[-1])+", "+str(line[dico['url']])+", "+str(line[dico['nom_monument']])+", "+str(line[dico['description']])+", "+str(line[dico['nom_commune']])+", "+str(line[dico['geoloc']])+");")
	output.write('\n')

def splitline(line):
	tab = []
	skip = False
	string = ""
	for char in line :
		if char == ';' and not skip:
			if (string != ""):
				tab.append(chr(39)+string+chr(39))
			else :
				tab.append("NULL")
			string = ""
		elif char == '"':
			if skip:
				skip = False
			else:
				skip = True
		elif char == chr(39):
			continue
		else :
			string += char
	if (string != ""):
		tab.append(chr(39)+string+chr(39))
	else :
		tab.append("NULL")
	return tab

dico = {"nom_image" : 17, "url" : 17, "nom_monument" : 6, "description" : 12, "nom_commune" : 8, "geoloc" : 19, "code_dept" : 25, "nom_dept" : 26, "nom_region" : 24}
code_dept_list = {}
with open('photographies_monuments.csv','r') as file:
	with open('insert_in_db.sql', 'w') as output:
		csvFile = csv.reader(file, delimiter=',')
		limit = 10
		firstline = True
		for line in csvFile:
			if firstline:
				firstline = False
				continue
			line = ','.join(line)
			line = splitline(line)
			if line[dico["code_dept"]] in code_dept_list:
				code_dept_list[line[dico["code_dept"]]] += 1
			else :
				code_dept_list[line[dico["code_dept"]]] = 1
			if limit > code_dept_list[line[dico["code_dept"]]] and line[dico["nom_commune"]] != "NULL" and line[dico["nom_image"]] != "NULL":
				Insert_SQL(line)
		print(code_dept_list)

		