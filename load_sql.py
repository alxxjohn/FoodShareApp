import os
import psycopg2


SCRIPTS_DIR = "./sql_scripts"


DB_NAME = os.getenv("POSTGRES_DB", "foodshare")
DB_USER = os.getenv("POSTGRES_USER", "postgres")
DB_PASS = os.getenv("POSTGRES_PASSWORD", "postgres")
DB_HOST = os.getenv("DB_HOST", "db")


def run_scripts():
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASS, host=DB_HOST
    )
    cur = conn.cursor()

    for filename in sorted(os.listdir(SCRIPTS_DIR)):
        if filename.endswith(".sql"):
            with open(os.path.join(SCRIPTS_DIR, filename), "r") as f:
                print(f"📄 Executing {filename}")
                cur.execute(f.read())
    conn.commit()
    cur.close()
    conn.close()
    print("✅ All SQL scripts loaded.")


if __name__ == "__main__":
    run_scripts()