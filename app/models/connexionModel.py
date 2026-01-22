from pydantic import BaseModel
from .executequerries import select, execute_other_query, get_cursor
import hashlib, hmac, os, secrets
import psycopg2
from psycopg2 import sql


class User(BaseModel):
	id_utilisateur: int
	pseudo: str
	email: str
	mdp_hash: str = None
	fournisseur_oauth: str = None
	id_oauth: str = None


SECRET_KEY = os.getenv("APP_SECRET_KEY", secrets.token_urlsafe(32))


def hash_password(password: str) -> str:
	# simple salted hash (use bcrypt/scrypt/argon2 in production)
	salt = SECRET_KEY[:16].encode()
	return hmac.new(salt, password.encode(), hashlib.sha256).hexdigest()


def verify_password(password: str, hashed: str) -> bool:
	return hmac.compare_digest(hash_password(password), hashed)


# Simple token store (in-memory); replace with JWT or DB-backed tokens in production
TOKENS: dict[str, int] = {}  # token -> user_id


def create_token_for_user(user: User) -> str:
	token = secrets.token_urlsafe(32)
	TOKENS[token] = user.id
	return token


def get_user_by_token(token: str) -> User:
	user_id = TOKENS.get(token)
	if not user_id:
		return None
	return get_user_by_id(user_id)


def get_user_by_name(name: str):
	print("entree dans getuserbyname")
	print(f"pseudo : {name}")
	list_user = select('utilisateur', where=f"pseudo='{name}'")
	print(f"list_user : {list_user}")
	return list_user


def save_user_to_db(username: str, password: str):
	print("entree dans save user to db")
	print(f"username : {username}, password : {password}")
	password_hashed = hash_password(password)
	conn, cursor = get_cursor()
	try:
		query = sql.SQL('INSERT INTO Utilisateur(pseudo, hashcode) VALUES ({u}, {p}) RETURNING id_utilisateur').format(
			u=sql.Literal(username),
			p=sql.Literal(password_hashed))
		print("saveusertodb : query bien crée")
		cursor.execute(query)
		id = int(cursor.fetchone()['id_utilisateur'])
		print(f"id : {id}")
		id_role = int(select('role', 'id_role', where=f"nom_role='Joueur'")[0]['id_role'])
		print(f"id du role : {id_role}")
		query = sql.SQL("INSERT INTO role_utilisateur (id_role, id_utilisateur) VALUES ({idr}, {id})").format(id=sql.Literal(id),
																											  idr = sql.Literal(id_role))
		cursor.execute(query)
		conn.commit()
		return True
	except Exception as e:
		print(f"Erreur de bd : {e}")
		return False


def logIn(user: User):
	pass


pass
