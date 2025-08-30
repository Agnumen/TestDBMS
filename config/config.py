from pydantic import BaseModel, field_validator, Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Set, Optional

"""    
    
class BotModel(BaseModel):
    # Bot
    token: str = Field(..., alias="BOT_TOKEN")
    admin_ids: str = Field(..., alias="BOT_ADMIN_IDS")
    payment_token: Optional[str] = Field(None, alias="BOT_PAYMENT_TOKEN")# Field(pattern=r"^\d{9}:(?:TEST|LIVE):\d{6}$")

    @field_validator('admin_ids', mode="before")
    def parse_admin_ids(cls, v):
        if isinstance(v, str):
            return set(int(x.strip()) for x in v.split(","))
        return v
    
class DBModel(BaseModel):
    # Database
    name: str = Field(..., alias="DB_NAME")
    host: str = Field(..., alias="DB_HOST")
    port: int = Field(..., alias="DB_PORT")
    user: str = Field(..., alias="DB_USER")
    password: str = Field(..., alias="DB_PASSWORD")
    
    # SQLite db
    sqlite: str = Field(..., alias="SQLITE_DB")
    
    def get_db_url(self):
        return (
            f"postgresql+asyncpg://{self.user}:{self.password}@"
            f"{self.host}:{self.port}/{self.name}"
        )
    
    def get_sqlite_db_url(self):
        return f"sqlite+aiosqlite:///{self.sqlite}.db"
    
    
class PGAdminModel(BaseModel):
    # PGAdmin
    PGADMIN_DEFAULT_EMAIL: str
    PGADMIN_DEFAULT_PASSWORD: str
    PGADMIN_PORT: int
    
class RedisModel(BaseModel):
    # Redis    
    REDIS_DB_NUM: int
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USERNAME: str
    REDIS_PASSWORD: str
"""
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
    
    def get_sqlite_db_url(self):
        return f"sqlite+aiosqlite:///{self.SQLITE_DB}.db"

    
    
settings = Settings()