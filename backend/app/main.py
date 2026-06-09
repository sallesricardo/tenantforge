import asyncio
from sqlalchemy import text
from fastapi import FastAPI
from contextlib import asynccontextmanager
from logSetup import LoggerSetup
from core.settings import settings
from db.database import get_db, engine
from api.v1.health import router as health_router

logger = LoggerSetup(settings.app_name, settings.log.level).getInstance()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Inicialização: a engine (e seu pool) está pronta para uso
    print("Iniciando a aplicação... Pool de conexões ativo.")
    yield
    # Encerramento: fecha todas as conexões do pool
    print("Encerrando a aplicação... Desligando o pool de conexões.")
    await engine.dispose()

app = FastAPI(
    lifespan=lifespan,
    title=settings.app_name,
)

app.include_router(health_router)


async def test_db():
    # get_db é um gerador assíncrono – iteramos para obter a sessão
    async for session in get_db():
        try:
            result = await session.execute(text("SELECT 1"))
            print("✅ Via get_db:", result.scalar())
            print(f"✅ Conexão bem-sucedida! Status do pool: {engine.pool.status()}")
        except Exception as e:
            print(f"❌ Erro: {e}")
        finally:
            # O gerador cuida do fechamento quando sair do loop
            break   # sai após a primeira sessão


def main():
    print(f"Hello from tenantforge ({settings.app_name})!")
    logger.info("Application started successfully.", extra={"user": "admin"})
    asyncio.run(test_db())


if __name__ == "__main__":
    main()
