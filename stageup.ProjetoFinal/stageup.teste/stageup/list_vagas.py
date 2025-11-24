#!/usr/bin/env python3
import sqlite3
import sys

con = sqlite3.connect('../instance/stageup.db')
cur = con.cursor()
cur.execute("SELECT id, codigo_vaga, titulo, empresa FROM vaga ORDER BY codigo_vaga")
rows = cur.fetchall()

print(f'Total vagas no banco: {len(rows)}')
print('=' * 100)
for i, (id, codigo, titulo, empresa) in enumerate(rows, 1):
    print(f"{i}. ID={id} | Codigo={codigo} | {titulo} | {empresa}")
print('=' * 100)

con.close()
sys.exit(0)
