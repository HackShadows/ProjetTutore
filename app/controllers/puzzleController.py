import unicodedata
from models.puzzleModel import save_image_to_db, getImagesUser, deleteImageById, selectImageByDept, selectImageById, selectMonumentNameById

def registerImage(nom_image: str,url: str, username: str):
	return save_image_to_db(nom_image, url, username)

def getAllPuzzleFromUser(usename: str):
	return getImagesUser(usename)

def deleteImage(image_id: str):
	return deleteImageById(image_id)

def getImageDept(dept_id: str):
	return selectImageByDept(dept_id)

def getImageById(image_id: str):
	return selectImageById(image_id)

def getHashSolution(tiles, size):
	print(tiles)
	print(size)
	res = ""
	offset = 13
	char = 0
	for tile in tiles:
		char = (tile['y'] + 1 ) * size + tile['x'] + 1 + tile['rotation']
		print(char)
		res += chr(char + offset)
	print(res)
	return res

def getMonumentNameById(id_image: str):
	return selectMonumentNameById(id_image)

def clean_string(text):
	# Passage en minuscule et retrait des accents
	text = ''.join((c for c in unicodedata.normalize('NFD', text.lower()) if unicodedata.category(c) != 'Mn'))
	return text.replace("-", "").replace(" ", "").replace("'", "")


