import psycopg2

def get_connection():
    return psycopg2.connect(
        host='ep-delicate-truth-ab60ob3h-pooler.eu-west-2.aws.neon.tech',
        database='neondb',
        user='neondb_owner',
        password='npg_o3JNrPmGx2td',
    )

def get_cursor():
    conn = get_connection()
    return conn.cursor()

cursor = get_cursor()
print("connected")
