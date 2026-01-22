
from models.connexionModel import hash_password, User, get_user_by_name, save_user_to_db

def registerUser(username: str, password: str, confirm_password: str):
	print("entree dans registerUser")
	print(f"username : {username}, password : {password}, confirm : {confirm_password}")
	if password != confirm_password:
		return False, "Les deux mots de passe ne sont pas identiques"

	if get_user_by_name(username):
		return False, "Le pseudo est déjà pris"

	try:
		save_user_to_db(username, password)
		return True, "Utilisateur inscrit"
	except Exception as e:
		return False, f"Erreur de base de donnée : {str(e)}"







