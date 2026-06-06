from config import settings
from logSetup import LoggerSetup
from database import get_db
from sqlalchemy import text

logger = LoggerSetup(settings.app_name, settings.log.level).getInstance()

def main():
    print(f"Hello from tenantforge ({settings.app_name})!")
    logger.info("Application started successfully.", extra={"user": "admin"})
    db = get_db()
    conn = next(db)
    result = conn.execute(text("SELECT 1"))
    print(result.fetchall())
    db.close()


if __name__ == "__main__":
    main()
