import os
import sqlite3

# Path ao banco
db_path = '../instance/stageup.db'

# Tentar apagar se existir
try:
    if os.path.exists(db_path):
        os.remove(db_path)
        print(f'✓ Arquivo {db_path} removido.')
except Exception as e:
    print(f'✗ Erro ao remover: {e}')

# Criar novo banco e tabela vaga vazia
try:
    con = sqlite3.connect(db_path)
    cur = con.cursor()
    
    # Criar tabela vaga (se não existir)
    cur.execute('''
        CREATE TABLE IF NOT EXISTS vaga (
            id INTEGER PRIMARY KEY,
            titulo VARCHAR(255) NOT NULL,
            empresa VARCHAR(255),
            cidade VARCHAR(100),
            estado VARCHAR(2),
            tipo_periodo VARCHAR(50),
            modalidade VARCHAR(50),
            salario VARCHAR(100),
            horario VARCHAR(100),
            descricao TEXT,
            link_ciee VARCHAR(500),
            area VARCHAR(100),
            codigo_vaga VARCHAR(50),
            created_at DATETIME
        )
    ''')
    con.commit()
    print('✓ Tabela vaga criada/verificada.')
    con.close()
except Exception as e:
    print(f'✗ Erro ao criar tabela: {e}')

print('✓ Banco limpo e pronto para inserção.')
