import csv

def Insert_SQL(line):
	output.write("INSERT INTO `Image` (`nom_image`,`url`,`nom_monument`,`description`,`nom_commune`,`geoloc`) VALUES ("+str(line[dico['nom_image']].split('/')[-1])+", "+str(line[dico['url']])+", "+str(line[dico['nom_monument']])+", "+str(line[dico['description']])+", "+str(line[dico['nom_commune']])+", "+str(line[dico['geoloc']])+")")
	output.write('\n')
	output.write("INSERT INTO `Lieu` (`nom_commune`,`code_dept`,`nom_dept`,`nom_region`) VALUES ("+str(line[dico['nom_commune']])+", "+str(line[dico['code_dept']])+", "+str(line[dico['nom_dept']])+", "+str(line[dico['nom_region']])+")")
	output.write('\n\n')

def splitline(line):
	tab = []
	skip = False
	string = ""
	for char in line :
		if char == ';' and not skip:
			if (string != ""):
				tab.append(string)
			else :
				tab.append("NULL")
			string = ""
		elif char == '"':
			if skip:
				skip = False
			else:
				skip = True
		else :
			string += char
	if (string != ""):
		tab.append(string)
	else :
		tab.append("NULL")
	return tab

dico = {"nom_image" : 17, "url" : 17, "nom_monument" : 6, "description" : 12, "nom_commune" : 8, "geoloc" : 19, "code_dept" : 25, "nom_dept" : 26, "nom_region" : 24}
with open('photographies_monuments.csv','r') as file:
	with open('insert_in_db.sql', 'w') as output:
		csvFile = csv.reader(file, delimiter=',')
		limit = 0
		firstline = True
		for line in csvFile:
			if firstline:
				firstline = False
				continue
			line = ','.join(line)
			line = splitline(line)
			Insert_SQL(line)

		