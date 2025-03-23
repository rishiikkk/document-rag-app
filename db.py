import asyncpg

DB_CONFIG = {
    "user": "your_username",
    "password": "your_password",
    "database": "rag_db",
    "host": "localhost",
    "port": 5432
}

async def create_db_connection():
    return await asyncpg.connect(**DB_CONFIG)

async def create_table():
    conn = await create_db_connection()
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS documents (
            id SERIAL PRIMARY KEY,
            filename TEXT,
            content TEXT,
            embedding BYTEA
        )
    ''')
    await conn.close()
