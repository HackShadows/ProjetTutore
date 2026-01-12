import csv

def Insert_SQL(line):
	#output.write("INSERT INTO `Image` (`nom_image`,`url`,`nom_monument`,`description`,`nom_commune`,`geoloc`) VALUES ("+str()+","+str()+","+str()+","+str(line[12])+","+str(line[8])+","+str()+")")
	#output.write(str(line) + '\n')
	#output.write("INSERT INTO `Lieu` (`nom_commune`,`code_dept`,`nom_dept`,`nom_region`) VALUES ("+str(line[8])+","+str(line[3])+","+str()+","+str()+")")
	#output.write(str(line) + '\n')
	print(len(line))

def splitline(line):
	tab = []
	string = ""
	for char in line :
		if char == ';':
			print(string)
			if (string != ""):
				tab.append(string)
			else :
				tab.append("NULL")
			string = ""
			
		else :
			string += char
	return tab

#dico = {"nom_image":,"url":21,"nom_monument":,"description"12:,"nom_commune":8,"geoloc":19,"code_dept":3,"nom_dept":,"nom_region":24,}
with open('photographies_monuments.csv','r') as file:
	with open('insert_in_db.sql', 'w') as output:
		csvFile = csv.reader(file, delimiter=',')
		limit = 0
		for line in csvFile:
			print(line)
			line = ';'.join(line)
			print(line)
			line = splitline(line)
			for i in range(len(line)):
				print(i,line[i])
			print(line)
			limit += 1
			if limit == 2:
				break	
			#Insert_SQL(line)

		