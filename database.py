from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import DeclarativeBase

# first we are using a sqlite database, but we can change this to any other database by changing the connection string
# sqlite is just a local file
SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./blog.db"

# Database URL ->   Engine -> Session Factory -> Sessions -> ORM Operations

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False)

#parent base class for all orm models to inherit from
class Base(DeclarativeBase):
    pass

# dependency to get a database session for each request
# we will use this for dependency injection in our routes
# what is dependency injection? 
# it is like providing req. objects/func to other function automatically when needed, instead of having to create them manually in each function
async def get_db():
    async with AsyncSessionLocal() as session:
        yield session