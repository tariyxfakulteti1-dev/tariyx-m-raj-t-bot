import sys
import os
import asyncio
import logging
from aiohttp import web
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.types import BotCommand
from aiogram.exceptions import TelegramNetworkError

from config import BOT_TOKEN
from handlers.start import router as start_router
from handlers.form import router as form_router

logging.basicConfig(level=logging.INFO)


# Render portyn ashıw ushın ápiwayı web-server
async def handle(request):
    return web.Response(text="Bot is running successfully!")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render avtomat beretuǵın PORT oqıp alınadı
    port = int(os.environ.get("PORT", 10000))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    print(f"🌐 Web-server {port}-portta iske tústi...")


async def set_bot_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="🔄 Bottı iske túsiriw"),
    ]
    try:
        await bot.set_my_commands(commands)
    except Exception as e:
        print(f"⚠️ Buyruqlardı ornatıwda qátelik ketti: {e}")


async def main():
    if not BOT_TOKEN:
        raise ValueError("BOT_TOKEN tabılmadı! config.py faylın tekseriń.")

    # 1. Render portın ashıw ushın web serverdi start etemiz
    await start_web_server()

    # 2. Bot session hám dispatcher
    session = AiohttpSession(timeout=60)

    bot = Bot(
        token=BOT_TOKEN,
        session=session,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML)
    )
    
    dp = Dispatcher()

    dp.include_router(start_router)
    dp.include_router(form_router)

    await set_bot_commands(bot)

    print("✅ Bot iske tústi...")
    
    try:
        await bot.delete_webhook(drop_pending_updates=True)
    except TelegramNetworkError:
        print("⚠️ Telegram serverine ulanıwda wazıypa úzildi, kútilip atır...")

    await dp.start_polling(bot)


if __name__ == "__main__":
    if sys.platform == 'win32':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("❌ Bot toqtatıldı!")
