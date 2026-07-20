import psycopg2
import sys
import os

# Try with LATIN9 encoding first (common on Windows Portuguese systems)
os.environ['PGCLIENTENCODING'] = 'LATIN9'

try:
    print('Tentando conectar ao PostgreSQL...')
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        user='postgres',
        password='985236',
        database='postgres',
        client_encoding='LATIN9'
    )
    print('Conexão bem-sucedida ao PostgreSQL')
    cursor = conn.cursor()
    cursor.execute('SELECT datname FROM pg_database WHERE datname = %s', ('Dash_Estoque',))
    result = cursor.fetchone()
    if result:
        print('Database Dash_Estoque existe')
    else:
        print('Database Dash_Estoque NÃO existe - criando...')
        conn.autocommit = True
        cursor.execute('CREATE DATABASE "Dash_Estoque"')
        print('Database Dash_Estoque criada com sucesso')
    cursor.close()
    conn.close()
except psycopg2.OperationalError as e:
    print(f'Erro de conexão: {e}')
    print('PostgreSQL não está rodando ou credenciais incorretas')
except UnicodeDecodeError as e:
    print(f'Erro de codificação UTF-8: {e}')
    print('Tente verificar a configuração de locale do PostgreSQL')
except Exception as e:
    print(f'Erro: {type(e).__name__}: {e}')
    import traceback
    traceback.print_exc()
