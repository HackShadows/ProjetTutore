import psycopg2
from psycopg2 import sql
from psycopg2.extras import RealDictCursor

def get_connection():
    return psycopg2.connect(
        host='ep-delicate-truth-ab60ob3h-pooler.eu-west-2.aws.neon.tech',
        database='neondb',
        user='neondb_owner',
        password='npg_o3JNrPmGx2td',
    )

def get_cursor():
    conn = get_connection()
    return conn, conn.cursor(cursor_factory=RealDictCursor)

conn, cursor = get_cursor()
print("connected")
#
# try:
#     # Vider la table pour libérer de l'espace
#     cursor.execute("TRUNCATE TABLE rawdata;")
#     conn.commit()
#     print("Table rawdata vidée avec succès.")
# except Exception as e:
#     print(e)
#
# with open("../photographies_monuments.csv", "r", encoding="utf-8") as f:
#     cursor.copy_expert(
#         "COPY rawdata FROM STDIN WITH (FORMAT csv, HEADER true, DELIMITER ';')",
#         f
#     )
#     conn.commit()

