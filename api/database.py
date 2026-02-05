import psycopg2

def get_connection():
    return psycopg2.connect(
        host="localhost",
        port=5432,
        dbname="shapes_db",
        user="postgres",
        password="postgres"
    )

def insert_features(table, features):
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(f"""
        INSERT INTO {table} 
        (area, perimeter, aspect_ratio, solidity, circularity, hu_moments)
        VALUES (%s,%s,%s,%s,%s,%s)
    """, (
        features["area"],
        features["perimeter"],
        features["aspect_ratio"],
        features["solidity"],
        features["circularity"],
        features["hu_moments"].tolist()
    ))

    conn.commit()
    cur.close()
    conn.close()

def fetch_all(table):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {table}")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows
