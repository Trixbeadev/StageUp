import sqlite3
from pathlib import Path

# Arquivos DB a checar
paths = [
    Path('..\..\instance\stageup.db').resolve(),
    Path('..\instance\stageup.db').resolve(),
    Path('instance\stageup.db').resolve(),
]
codes = ['5859313','5859771','5859754','5859274','5858881','5859045','5858612','5858529','5858502','5858494','5858446','5858258','5857773','5861134']

for p in paths:
    print('\nChecking DB:', p)
    if not p.exists():
        print('  NOT FOUND')
        continue
    try:
        conn = sqlite3.connect(str(p))
        cur = conn.cursor()
        # check if table exists
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vaga'")
        if not cur.fetchone():
            print('  table `vaga` not found')
            conn.close()
            continue
        for code in codes:
            cur.execute('SELECT COUNT(*) FROM vaga WHERE codigo_vaga=?', (code,))
            cnt = cur.fetchone()[0]
            if cnt:
                print(f'  {code}: {cnt}')
        conn.close()
    except Exception as e:
        print('  ERROR:', e)

print('\nDone')
