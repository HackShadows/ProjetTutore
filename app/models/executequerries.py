from connexion import *


def SelectAll(query, params=None):
    try:
        cursor.execute(query, params or ())
        return cursor.fetchall()
    except Exception as e:
        print("Database error:", e)
        return []


def SelectOne(query, params=None):
    try:
        cursor.execute(query, params or ())
        return cursor.fetchone()
    except Exception as e:
        print("Database error:", e)
        return None

conn, cursor = get_cursor()
print(SelectAll("SELECT * FROM Lieu"))
