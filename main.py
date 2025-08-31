import asyncio

from app import main
from config import settings

asyncio.run(main(settings))
