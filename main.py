import asyncio
from config import settings
from logSetup import LoggerSetup
from database import get_db
from sqlalchemy import text
import time

logger = LoggerSetup(settings.app_name, settings.log.level).getInstance()

async def test_db():
    # get_db é um gerador assíncrono – iteramos para obter a sessão
    async for session in get_db():
        try:
            result = await session.execute(text("SELECT 1"))
            print("✅ Via get_db:", result.scalar())
        finally:
            # O gerador cuida do fechamento quando sair do loop
            break   # sai após a primeira sessão


def main():
    print(f"Hello from tenantforge ({settings.app_name})!")
    logger.info("Application started successfully.", extra={"user": "admin"})
    asyncio.run(test_db())


if __name__ == "__main__":
    main()
