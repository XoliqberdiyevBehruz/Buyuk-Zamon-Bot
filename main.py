import asyncio, logging, sys

from aiogram import Bot, Dispatcher

import config 
from handlars import common


bot = Bot(config.BOT_TOKEN)

async def main():
    db = Dispatcher()

    db.include_router(
        common.router,
    )

    await db.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())