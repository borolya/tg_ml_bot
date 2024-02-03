from aiogram import Bot, Dispatcher
import asyncio
import logging

from config.config import load_config
from keyboards.keyboards import set_menu
from handlers.handlers_cmd import rt_commands, storage
from handlers.handlers_callback import rt_callbacks

logger = logging.getLogger(__name__)


async def main():
    logging.basicConfig(
        level=logging.DEBUG,
        format='[{asctime}] #{levelname:8} {filename}:'
               '{lineno} - {name} - {message}',
        style='{'
    )
    logger.info("Bot starting")
    bot = Bot(load_config().token)
    dp = Dispatcher(storage=storage)

    await set_menu(bot)

    dp.include_router(rt_commands)
    dp.include_router(rt_callbacks)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
