import sqlite3
import os

db_path = os.path.join("database", "forge_x_ai.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT id, name, email, role FROM users")
users = c.fetchall()
print("=== USERS ===")
for u in users:
    print(f"  ID={u[0]}, Name={u[1]}, Email={u[2]}, Role={u[3]}")

c.execute("SELECT COUNT(*) FROM leads")
print(f"\n=== LEADS: {c.fetchone()[0]} ===")
c.execute("SELECT stage, COUNT(*) FROM leads GROUP BY stage")
for row in c.fetchall():
    print(f"  {row[0]}: {row[1]}")

c.execute("SELECT COUNT(*) FROM ai_recommendations")
print(f"\n=== AI RECOMMENDATIONS: {c.fetchone()[0]} ===")

c.execute("SELECT COUNT(*) FROM follow_up_history")
print(f"=== FOLLOW-UPS: {c.fetchone()[0]} ===")

conn.close()
