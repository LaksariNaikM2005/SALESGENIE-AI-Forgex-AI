"""
Update lead stages based on ML score ranges:
- Won:         lead_score >= 75
- Negotiation: 70 <= lead_score < 75
- Proposal:    50 <= lead_score < 70
- Qualified:   25 <= lead_score < 50
- New Lead:    lead_score < 25
"""
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import sqlite3

db_path = os.path.join("database", "forge_x_ai.db")
conn = sqlite3.connect(db_path)
c = conn.cursor()

c.execute("SELECT id, lead_score FROM leads ORDER BY id")
leads = c.fetchall()
print(f"Total leads: {len(leads)}")

for lead_id, score in leads:
    score_val = float(score or 0.0)
    if score_val >= 75.0:
        stage = "Won"
        status = "Closed"
    elif score_val >= 70.0:
        stage = "Negotiation"
        status = "Open"
    elif score_val >= 50.0:
        stage = "Proposal"
        status = "Open"
    elif score_val >= 25.0:
        stage = "Qualified"
        status = "Open"
    else:
        stage = "New Lead"
        status = "Open"

    c.execute("UPDATE leads SET stage=?, status=? WHERE id=?", (stage, status, lead_id))

conn.commit()

c.execute("SELECT stage, COUNT(*) FROM leads GROUP BY stage ORDER BY COUNT(*) DESC")
print("\nStage distribution based on ML Score thresholds:")
for row in c.fetchall():
    print(f"  {row[0]:15s}: {row[1]:5d}")

conn.close()
print("\nStage update complete!")
