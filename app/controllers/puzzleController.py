from models.puzzleModel import save_image_to_db, getImagesUser, deleteImageById, selectImageByDept

def registerImage(nom_image: str,url: str, username: str):
	return save_image_to_db(nom_image, url, username)

def getAllPuzzleFromUser(usename: str):
	return getImagesUser(usename)

def deleteImage(id: str):
	return deleteImageById(id)

def getImageDept(id: str):
	return selectImageByDept(id)