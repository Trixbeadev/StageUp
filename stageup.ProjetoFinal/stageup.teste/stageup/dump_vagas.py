import sqlite3
con = sqlite3.connect('../instance/stageup.db')
cur = con.cursor()
cur.execute("SELECT titulo, empresa, cidade, salario FROM vaga ORDER BY codigo_vaga")
rows = cur.fetchall()
with open('vagas_dump.txt', 'w', encoding='utf-8') as f:
    f.write(f'Total vagas: {len(rows)}\n')
    for r in rows:
        f.write('|'.join([str(x) if x is not None else '' for x in r]) + '\n')
con.close()
print('dump_vagas.py executed, output in vagas_dump.txt')