import asyncio
# import logging

from app import main
from config import settings

asyncio.run(main(settings))