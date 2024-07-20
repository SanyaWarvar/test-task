from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher
from config import TOKEN_BOT_API
from handlers import router as handle_router


async def main():
    bot = Bot(token=TOKEN_BOT_API, default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()
    dp.include_router(handle_router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)
