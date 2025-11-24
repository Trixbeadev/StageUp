import sqlite3
from pathlib import Path

db_path = Path('../instance/stageup.db')
if not db_path.exists():
    print(f"DB não encontrado em: {db_path}")
    raise SystemExit(1)

conn = sqlite3.connect(str(db_path))
cur = conn.cursor()

codes = ('5859819','5859771','5859980','5859313','5859771','5859754','5859274','5858881','5859045','5858612','5858529','5858502','5858494','5858446','5858258','5857773','5861134')
placeholders = ','.join('?' for _ in codes)
q = f"SELECT id,titulo,empresa,cidade,estado,salario,descricao,link_ciee,codigo_vaga,created_at FROM vaga WHERE codigo_vaga IN ({placeholders})"
cur.execute(q, codes)
rows = cur.fetchall()
if not rows:
    print('Nenhuma vaga encontrada com os códigos solicitados.')
else:
    for r in rows:
        id,titulo,empresa,cidade,estado,salario,descricao,link,code,created_at = r
        print('---')
        print(f'id: {id}')
        print(f'codigo_vaga: {code}')
        print(f'titulo: {titulo}')
        print(f'empresa: {empresa}')
        print(f'local: {cidade}, {estado}')
        print(f'salario: {salario}')
        print(f'descricao (trecho): {(descricao or '')[:300]}')
        print(f'link_ciee: {link}')
        print(f'created_at: {created_at}')

conn.close()
