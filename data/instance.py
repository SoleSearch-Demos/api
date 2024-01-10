import os

import motor.motor_asyncio
from dotenv import dotenv_values

config = {**dotenv_values("db.env"), **os.environ}
DESCENDING = -1
ASCENDING = 1

client = motor.motor_asyncio.AsyncIOMotorClient(config.DB_URL)
db = client[config.NAME]
sneakers = db[config.SNEAKERS_COLLECTION]