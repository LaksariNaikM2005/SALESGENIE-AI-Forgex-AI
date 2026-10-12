import getpass
import psycopg
from psycopg import sql

admin_password = getpass.getpass("PostgreSQL admin password: ")
app_password = getpass.getpass("New salesgenie application password: ")

with psycopg.connect(
    host="localhost",
    port=5432,
    dbname="postgres",
    user="postgres",
    password=admin_password,
    autocommit=True,
) as conn:
    with conn.cursor() as cur:
        cur.execute(
            "SELECT 1 FROM pg_roles WHERE rolname = %s",
            ("salesgenie",),
        )
        if cur.fetchone() is None:
            cur.execute(
                sql.SQL("CREATE ROLE {} LOGIN PASSWORD {}").format(
                    sql.Identifier("salesgenie"),
                    sql.Literal(app_password),
                )
            )
            print("Created application role.")
        else:
            print("Application role already exists; no role changes made.")

        cur.execute(
            "SELECT 1 FROM pg_database WHERE datname = %s",
            ("salesgenie",),
        )
        if cur.fetchone() is None:
            cur.execute(
                sql.SQL("CREATE DATABASE {} OWNER {}").format(
                    sql.Identifier("salesgenie"),
                    sql.Identifier("salesgenie"),
                )
            )
            print("Created salesgenie database.")
        else:
            print("Database already exists; no database changes made.")

print("Setup checks completed.")
