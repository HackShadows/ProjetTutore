from models.puzzleModel import save_image_to_db, getImagesUser

def registerImage(nom_image: str, nom_monument: str, description: str, nom_commune: str, longitude: str,
					 latitude: str, url: str, username: str):
	return save_image_to_db(nom_image, nom_monument, description, nom_commune, longitude, latitude, url, username)

def getAllPuzzleFromUser(usename: str):
	return getImagesUser(usename)