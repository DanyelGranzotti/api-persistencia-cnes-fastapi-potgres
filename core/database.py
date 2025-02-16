from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from core.config import settings

# Async engine for normal operations
engine = create_async_engine(settings.DATABASE_URL, echo=True)
async_session = sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

# Sync engine for migrations and schema generation
sync_engine = create_engine(settings.SYNC_DATABASE_URL, echo=True)

Base = declarative_base()

async def get_db() -> AsyncSession:
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            print(f"Database error: {str(e)}")  # Add logging for debugging
            raise
        finally:
            await session.close()

async def init_models():
    try:
        # Import here to avoid circular imports
        from scripts.create_database import create_database
        
        # Ensure database exists
        await create_database()
        
        # Continue with existing initialization
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
    except Exception as e:
        print(f"Error initializing models: {e}")
        raise
