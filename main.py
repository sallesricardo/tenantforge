from config import settings
from logSetup import LoggerSetup

logger = LoggerSetup(settings.app_name, settings.log.level).getInstance()

def main():
    print(f"Hello from tenantforge ({settings.app_name})!")
    logger.info("Application started successfully.", extra={"user": "admin"})


if __name__ == "__main__":
    main()
