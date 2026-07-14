from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from typing import AsyncGenerator

load_dotenv()

DATABASE_URL=os.getenv("DATABASE_URL")
if DATABASE_URL and "?" in DATABASE_URL:
    # Split the URL at the '?' to separate the base credentials from the query arguments
    base_url, _ = DATABASE_URL.split("?", 1)
    DATABASE_URL = base_url

# Initialize the engine cleanly, passing ssl=True via connect_args
engine = create_async_engine(
    DATABASE_URL, 
    echo=False,
    connect_args={"ssl": True}  # Forces a secure SSL connection natively in asyncpg
)


Session=async_sessionmaker(

    bind=engine,
    autoflush=False,
    expire_on_commit=False


)

async def get_db_Session()->AsyncGenerator[AsyncSession,None]:

    async with  Session() as session:
        try:
            yield session
            await session.commit()
        except Exception as e:
            await session.rollback()
            raise     
        finally:
            await session.close()