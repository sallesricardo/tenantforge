from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from core.settings import settings

DRIVER = settings.database.driver
USER = settings.database.user
PASSWORD = settings.database.password
HOST = settings.database.host
PORT = settings.database.port
NAME = settings.database.name

DATABASE_URL = f"{DRIVER}://{USER}:{PASSWORD}@{HOST}:{PORT}/{NAME}"

DEBUG = settings.database.debug
POOL_SIZE = settings.database.pool.size
MAX_OVERFLOW = settings.database.pool.max_overflow
POOL_TIMEOUT = settings.database.pool.timeout
POOL_RECYCLE = settings.database.pool.recycle

engine = create_async_engine(
    DATABASE_URL,
    echo=DEBUG,                 # Log SQL (útil em desenvolvimento)
    future=True,                # Usa a API 2.0 do SQLAlchemy
    pool_size=POOL_SIZE,        # Número de conexões mantidas abertas (padrão: 5)
    max_overflow=MAX_OVERFLOW,  # Conexões extras além do pool_size (padrão: 10)[reference:3]
    pool_timeout=POOL_TIMEOUT,  # Segundos para esperar por uma conexão do pool (padrão: 30)[reference:4]
    pool_recycle=POOL_RECYCLE,  # Recicla conexões mais antigas que 1 hora (padrão: -1)[reference:5]
    pool_pre_ping=True,         # Verifica se a conexão está viva antes de usá-la (Recomendado!)[reference:6]
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
