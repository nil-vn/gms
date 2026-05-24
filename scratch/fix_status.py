import sqlite3
conn = sqlite3.connect('instance/db.sqlite3')
cur = conn.cursor()
cur.execute("UPDATE [transaction] SET status = 'PAID' WHERE status = 'paid'")
conn.commit()
print(f"Fixed {cur.rowcount} row(s)")
cur.execute("SELECT status, COUNT(*) FROM [transaction] GROUP BY status")
print(cur.fetchall())
conn.close()
