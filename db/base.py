from config.config import DATABASE_URL, DATABASE_NAME
import motor.motor_asyncio
from beanie import init_beanie

from models.box import Box


async def initiate_database():
    client = motor.motor_asyncio.AsyncIOMotorClient(DATABASE_URL)
    await init_beanie(database=client.get_dafault_database,
                      document_models=[Box])


