import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo
from aiohttp import web

BOT_TOKEN = os.getenv("BOT_TOKEN")
WEBAPP_URL = "https://promogame-webapp.vercel.app/index.html"

if not BOT_TOKEN:
    raise ValueError("Ошибка: BOT_TOKEN не задан в переменной окружения!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    campaign_id = command.args  
    if campaign_id:
        app_url = f"{WEBAPP_URL}?campaign_id={campaign_id}"
        text = f"👋 Привет, {message.from_user.first_name}!\n\n🎉 Вам доступна персональная промо-карточка!"
        button_text = "🎁 Стереть и получить подарок"
    else:
        app_url = WEBAPP_URL
        text = f"👋 Привет, {message.from_user.first_name}!\n\nЗапустите Mini App, чтобы участвовать в акциях!"
        button_text = "🎰 Открыть игральную карту"

    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button_text, web_app=WebAppInfo(url=app_url))]
    ])
    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

# --- Фейковый HTTP-сервер для удовлетворения требований Render Web Service ---
async def handle_ping(request):
    return web.Response(text="Bot is live!")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    
    # Render автоматически передает номер порта в переменную окружения PORT
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Dummy HTTP server started on port {port}")

# --- Основная функция запуска ---
async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Запускаем локальный веб-сервер параллельно с ботом
    await start_web_server()
    
    # Запускаем слушатель Telegram
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
