import os
import psycopg2

REQUIRED_TABLES = ["users", "businesses"]

DB_CONFIG = {
    "host": os.getenv("FOODSHAREAPP_API_DB_HOST", "foodshareapp-db"),
    "port": int(os.getenv("FOODSHAREAPP_API_DB_PORT", 5432)),
    "user": os.getenv("FOODSHAREAPP_API_DB_USER", "foodshareapp"),
    "password": os.getenv("FOODSHAREAPP_API_DB_PASS", "foodshareapp"),
    "dbname": os.getenv("FOODSHAREAPP_API_DB_BASE", "foodshareapp"),
}


def check_tables_exist():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        cur = conn.cursor()

        for table in REQUIRED_TABLES:
            cur.execute(
                """
                SELECT EXISTS (
                    SELECT FROM information_schema.tables 
                    WHERE table_schema = 'public' AND table_name = %s
                );
                """,
                (table,),
            )
            exists = cur.fetchone()[0]
            if not exists:
                raise Exception(f"❌ Table '{table}' does not exist!")

        cur.close()
        conn.close()
        print("✅ All required tables exist in the database.")

    except Exception as e:
        print(f"❌ Database check failed: {e}")
        exit(1)


if __name__ == "__main__":
    check_tables_exist()
