import getpass
import psycopg

password = getpass.getpass("PostgreSQL admin password: ")

try:
    with psycopg.connect(
        host="127.0.0.1",
        port=5432,
        dbname="postgres",
        user="postgres",
        password=password,
    ) as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT rolname, rolcanlogin FROM pg_roles WHERE rolname = %s",
                ("salesgenie",),
            )
            print("Role details:", cur.fetchall())

            cur.execute(
                "SELECT datname FROM pg_database WHERE datname = %s",
                ("salesgenie",),
            )
            print("Database details:", cur.fetchall())

except psycopg.Error as exc:
    print("PostgreSQL error:", exc)
