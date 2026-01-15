from connexion import *

def SelectAll(query):
    cursor = get_cursor()
    cursor.execute(query)
    rows = cursor.fetchall()
    return rows

def SelectOne(query):
    cursor = get_cursor()
    cursor.execute(query)
    rows = cursor.fetchone()
    return rows
