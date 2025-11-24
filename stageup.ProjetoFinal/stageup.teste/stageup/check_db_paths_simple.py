import sqlite3, os
paths = [r'c:\Users\beatr\OneDrive\Desktop\stageup.teste44\instance\stageup.db',
         r'c:\Users\beatr\OneDrive\Desktop\stageup.teste44\stageup.teste\instance\stageup.db',
         r'c:\Users\beatr\OneDrive\Desktop\stageup.teste44\stageup.teste\stageup\instance\stageup.db']
code='5861134'
for p in paths:
    print('\nDB:', p)
    print(' exists=', os.path.exists(p))
    if not os.path.exists(p):
        continue
    try:
        conn = sqlite3.connect(p)
        cur = conn.cursor()
        cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='vaga'")
        print(' has vaga table=', bool(cur.fetchone()))
        try:
            cur.execute('SELECT COUNT(*) FROM vaga WHERE codigo_vaga=?',(code,))
            print(code, 'count=', cur.fetchone()[0])
        except Exception as e:
            print(' query error:', e)
        conn.close()
    except Exception as e:
        print(' error open:', e)
print('\nDone')
