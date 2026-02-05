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
        INSERT INTO {table} (
            area, perimeter, aspect_ratio,
            solidity, circularity, orientation,
            hu_moments, histogram
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        features["area"],
        features["perimeter"],
        features["aspect_ratio"],
        features["solidity"],
        features["circularity"],
        features["orientation"],
        features["hu_moments"].tolist(),
        features["histogram"].tolist()
    ))

    conn.commit()
    cur.close()
    conn.close()
