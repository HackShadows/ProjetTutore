from .executequerries import select, execute_other_query, get_cursor
from psycopg2 import sql
from datetime import datetime, timedelta, UTC
from jose import jwt, JWTError
import bcrypt
import os


# Configuration JWT
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    """Crée un token JWT avec une expiration"""
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    # Le token contient les données + la date d'expiration
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def verify_token(token: str):
    """Vérifie le token et retourne le pseudo si valide"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            return None
        return username
    except JWTError:
        return None

#todo mieux stocker la chaine pour la génération des tokens
SECRET_KEY = os.getenv("APP_SECRET_KEY", "une_chaine_tres_secrete_et_fixe_pour_le_dev")


def hash_password(password: str) -> str:
    # On convertit le string en bytes, on hache, et on reconvertit en string pour le stockage BDD
    pwd_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(pwd_bytes, salt)
    return hashed.decode('utf-8')

def verify_password(password: str, hashed: str) -> bool:
    pwd_bytes = password.encode('utf-8')
    hashed_bytes = hashed.encode('utf-8')
    return bcrypt.checkpw(pwd_bytes, hashed_bytes)


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


def get_hashed_password(username):
    request = select('utilisateur', 'hashcode', where=f"pseudo='{username}'")
    return request[0]['hashcode'] if request else None


pass

'2adf20eff5486112aa2e7ebdd8fe71fe71d6e6004821285aaab76a30418fc657'
