from .executequerries import select, execute_other_query, get_cursor
from psycopg2 import sql
from random import randint


def save_image_to_db(nom_image: str, url: str, username: str):
	conn, cursor = get_cursor()
	try:
		requestUserId = select("utilisateur", 'id_utilisateur', where=f"pseudo='{username}'")
		if requestUserId:
			userId = requestUserId[0]['id_utilisateur']
		else:
			return
		query = sql.SQL('INSERT INTO image(nom_image, nom_monument, description, nom_commune, url, geoloc, public, id_utilisateur) '
						'VALUES ({ni}, null, null, null, {u}, null, FALSE, {id})').format(
			ni=sql.Literal(nom_image),
			u=sql.Literal(url),
			id=sql.Literal(userId))
		cursor.execute(query)
		conn.commit()
		return True, ""
	except Exception as e:
		print(f"Erreur de bd : {e}")
		return False, e


def getImagesUser(username: str):

	return select("image", ['id_image', 'nom_image', 'id_utilisateur',
			'nom_monument', 'description', 'nom_commune', 'geoloc', 'public', 'url'],
				  where=f"pseudo='{username}'", join="utilisateur", using="id_utilisateur")

def deleteImageById(id: str):
	conn, cursor = get_cursor()
	try:
		query = sql.SQL("DELETE FROM image WHERE id_image={id}").format(id=sql.Literal(id))
		cursor.execute(query)
		conn.commit()
		return True, ""
	except Exception as e:
		print(f"Erreur de bd : {e}")
		return False, e


def selectImageByDept(id: str):
	allImages = select('image', where=f"code_dept='{str(id)}' and public", join='lieu', using='nom_commune')
	randomIndex = randint(0, len(allImages)-1)
	return allImages[randomIndex] if len(allImages) > 0 else None

def selectImageById(id: str):
	image = select('image', where=f"id_image={id}")
	return image[0] if image else None

def get_department_info(dept_code: str):
	"""Récupère le nom du département dans la table Lieu."""
	conn, cursor = get_cursor()
	try:
		query = sql.SQL("SELECT nom_dept FROM lieu WHERE code_dept = {code} LIMIT 1").format(code=sql.Literal(dept_code))
		cursor.execute(query)
		result = cursor.fetchone()

		if result:
			return result['nom_dept']
		return "Inconnu"
	except Exception as e:
		print(f"Erreur SQL get_department_info : {e}")
		return "Inconnu"

def selectMonumentNameById(id_image: str):
	name = select('image', 'nom_monument', where=f"id_image={id_image}")
	return name[0] if name else None
