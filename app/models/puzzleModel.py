from .executequerries import select, execute_other_query, get_cursor
from psycopg2 import sql


def save_image_to_db(nom_image: str, nom_monument: str, description: str, nom_commune: str, longitude: str,
					 latitude: str, url: str, username: str):
	print("entree dans save image to db")
	conn, cursor = get_cursor()
	try:
		requestUserId = select("utilisateur", 'id_utilisateur', where=f"pseudo='{username}'")
		if requestUserId:
			userId = requestUserId[0]['id_utilisateur']
		else:
			return
		query = sql.SQL('INSERT INTO image(nom_image, nom_monument, description, nom_commune, url, geoloc, public, id_utilisateur) '
						'VALUES ({ni}, {nm}, {d}, {nc}, {u}, {g}, FALSE, {id}) RETURNING id_utilisateur').format(
			ni=sql.Literal(nom_image),
			nm=sql.Literal(nom_monument),
			d=sql.Literal(description),
			# nc=sql.Literal(nom_commune),
			nc=sql.NULL, # todo ajouter lieu si il existe pas
			u=sql.Literal(url),
			g=sql.Literal(str(longitude) + ', ' + str(latitude)),
			id=sql.Literal(userId))
		print("saveimagetodb : query bien crée")
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
	print("entree dans save image to db")
	conn, cursor = get_cursor()
	try:
		query = sql.SQL("DELETE FROM image WHERE id_image={id}").format(id=sql.Literal(id))
		print("deleteImagetodb : query bien crée")
		cursor.execute(query)
		conn.commit()
		return True, ""
	except Exception as e:
		print(f"Erreur de bd : {e}")
		return False, e

