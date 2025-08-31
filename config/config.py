from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    # Logging
    LOG_LEVEL: str
    LOG_FORMAT: str
    
    # Bot
    BOT_TOKEN: str
    BOT_ADMIN_IDS: str
    BOT_PAYMENT_TOKEN: Optional[str] = None
    
    # Database
    DB_NAME: str
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    
    # SQLite db
    SQLITE_DB: str
    
    # PGAdmin
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    PGADMIN_PORT: int
    
    # Redis    
    REDIS_DB_NUM: int
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )
    
    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    def get_db_url_sync(self):
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        
    def get_sqlite_db_url(self):
        return f"sqlite+aiosqlite:///{self.SQLITE_DB}.db"

    
    
settings = Settings()