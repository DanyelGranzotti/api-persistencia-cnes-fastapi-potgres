import asyncpg
import asyncio
from core.config import settings

async def create_database():
    try:
        # Connect to default postgres database first
        sys_conn = await asyncpg.connect(
            user=settings.POSTGRES_USER,
            password=settings.POSTGRES_PASSWORD,
            host=settings.POSTGRES_HOST,
            port=settings.POSTGRES_PORT,
            database='postgres'
        )
        
        # Check if our database exists
        exists = await sys_conn.fetchval(
            'SELECT 1 FROM pg_database WHERE datname = $1',
            settings.POSTGRES_DB
        )
        
        if not exists:
            # Create the database
            await sys_conn.execute(f'CREATE DATABASE {settings.POSTGRES_DB}')
            print(f"Database {settings.POSTGRES_DB} created successfully")
        else:
            print(f"Database {settings.POSTGRES_DB} already exists")
        
        await sys_conn.close()
        return True
    except Exception as e:
        print(f"Error creating database: {e}")
        return False

def main():
    asyncio.run(create_database())

if __name__ == "__main__":
    main()
