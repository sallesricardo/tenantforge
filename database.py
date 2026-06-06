from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base

# URL do PostgreSQL (síncrono)
DATABASE_URL = "postgresql+psycopg://postgres:password@localhost:5432/postgres"

engine = create_async_engine(
    DATABASE_URL,
    echo=True,                 # Log SQL (útil em desenvolvimento)
    future=True,              # Usa a API 2.0 do SQLAlchemy
)

AsyncSessionLocal = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,   # Evita expiração de objetos após commit
)

Base = declarative_base()

# Dependência para obter sessão do banco
async def get_db() -> AsyncSession:
    async with AsyncSessionLocal() as session:
        yield session
