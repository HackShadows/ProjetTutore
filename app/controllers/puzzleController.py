from models.puzzleModel import save_image_to_db, getImagesUser, deleteImageById, selectImageByDept, selectImageById

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

def getHashSolution(tiles):
	print(tiles)
	res = 0
	for tile in tiles:
		res += tile['y'] + 1
		res *= 7
		res += tile['x'] + 1
		res *= 7
		res += tile['rotation']
		res *= 7
	print(res)
	return res


