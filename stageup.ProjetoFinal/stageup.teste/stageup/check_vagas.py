import sqlite3
conn = sqlite3.connect('../instance/stageup.db')
cur = conn.cursor()
cur.execute("SELECT id, titulo, empresa, codigo_vaga FROM vaga ORDER BY id")
rows = cur.fetchall()
print(f'Total vagas: {len(rows)}')
for r in rows:
    print(r)
conn.close()