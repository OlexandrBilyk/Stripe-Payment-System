from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from app.core import DB_URL

engine = create_async_engine(DB_URL)

AsyncSessionLocal = async_sessionmaker(engine)

async def get_db():
    async with AsyncSessionLocal() as db:
        async with db.begin():
            yield db