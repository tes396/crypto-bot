import os
import psycopg2

print("DATABASE_URL:", DATABASE_URL)

try:
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("SELECT version();")
    version = cur.fetchone()
    print("Connected to:", version)

    cur.close()
    conn.close()

    print("SUCCESS: Database connection working")

except Exception as e:
    print("DB CONNECTION FAILED")
    print(str(e))
    raise


















