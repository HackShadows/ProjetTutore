import psycopg2

def get_connection():
    return psycopg2.connect(
        host="xa6wqy.h.filess.io",
        database="PuzzleTUT_itselfrise",
        user="PuzzleTUT_itselfrise",
        password="e3d0a6e5aef6f3874d530272672c6fd332e32f8c",
        port="61036"
    )

def get_cursor():
    conn = get_connection()
    return conn, conn.cursor()
