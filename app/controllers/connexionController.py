
from models.connexionModel import hash_password, get_user_by_name, save_user_to_db, get_hashed_password, verify_password, create_access_token


def registerUser(username: str, password: str, confirm_password: str):
	if password != confirm_password:
		return False, "Les deux mots de passe ne sont pas identiques"

	if username in ["None", "null"]:
		return False, f"{username} n'est pas un pseudo valide"

	if get_user_by_name(username):
		return False, "Le pseudo est déjà pris"

	try:
		save_user_to_db(username, password)
		return True, "Utilisateur inscrit"
	except Exception as e:
		return False, f"Erreur de base de donnée : {str(e)}"


def logIn(username: str, password: str):
	hashed_password = get_hashed_password(username)
	if hashed_password:
		if verify_password(password, hashed_password):
			print("Utilisateur connecté")
			token = create_access_token(data={'sub': username})
			return True, token
		print("Mot de passe incorrect")
		return False, "Mot de passe incorrect"
	else:
		print(f"Pas de compte trouvé pour cet utilisateur {username}")
		return False, f"Pas de compte trouvé pour cet utilisateur {username}"



