"""
Script para adicionar as colunas faltantes à tabela user no banco de dados.
Execute este script uma vez para atualizar o schema do banco de dados.
"""

import os
import sqlite3

# Caminho do banco de dados (mesmo caminho usado em app.py)
instance_dir = os.path.join(os.path.dirname(__file__), 'instance')
db_path = os.path.join(instance_dir, 'stageup.db')

def column_exists(cursor, table_name, column_name):
    """Verifica se uma coluna existe na tabela"""
    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = [row[1] for row in cursor.fetchall()]
    return column_name in columns

def update_user_table():
    """Adiciona as colunas faltantes à tabela user"""
    if not os.path.exists(db_path):
        print(f"[ERRO] Banco de dados nao encontrado em {db_path}")
        print("  O banco sera criado automaticamente na proxima execucao do app.")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar se a tabela user existe
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='user'")
        if not cursor.fetchone():
            print("[ERRO] Tabela 'user' nao existe. Ela sera criada automaticamente na proxima execucao.")
            conn.close()
            return
        
        # Lista de colunas para adicionar
        columns_to_add = [
            ('updated_at', 'DATETIME'),
            ('login_method', 'VARCHAR(20) DEFAULT "local"'),
            ('social_id', 'VARCHAR(255)')
        ]
        
        added_count = 0
        for column_name, column_def in columns_to_add:
            if not column_exists(cursor, 'user', column_name):
                try:
                    cursor.execute(f'ALTER TABLE user ADD COLUMN {column_name} {column_def}')
                    print(f"[OK] Coluna '{column_name}' adicionada com sucesso.")
                    added_count += 1
                except sqlite3.OperationalError as e:
                    print(f"[ERRO] Erro ao adicionar coluna '{column_name}': {e}")
            else:
                print(f"[INFO] Coluna '{column_name}' ja existe, pulando...")
        
        conn.commit()
        conn.close()
        
        if added_count > 0:
            print(f"\n[OK] {added_count} coluna(s) adicionada(s) com sucesso!")
            print("  Agora voce pode tentar se cadastrar novamente.")
        else:
            print("\n[OK] Todas as colunas ja existem. Nenhuma alteracao necessaria.")
            
    except Exception as e:
        print(f"[ERRO] Erro ao atualizar banco de dados: {e}")

if __name__ == '__main__':
    print("Atualizando tabela 'user' no banco de dados...")
    print(f"Caminho do banco: {db_path}\n")
    update_user_table()

