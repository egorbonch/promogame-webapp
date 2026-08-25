import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command, CommandObject
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo

BOT_TOKEN = os.getenv("BOT_TOKEN")
# Прямой адрес вашего сайта на Vercel или GitHub Pages
WEBAPP_URL = "https://promogame-webapp.vercel.app/index.html"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message(Command("start"))
async def start_handler(message: types.Message, command: CommandObject):
    # Telegram передает ID акции после команды /start (например: /start e4d291a8-...)
    campaign_id = command.args  

    if campaign_id:
        # Передаем ID акции как GET-параметр прямо в WebApp URL
        app_url = f"{WEBAPP_URL}?campaign_id={campaign_id}"
        
        text = (
            f"👋 Привет, {message.from_user.first_name}!\n\n"
            "🎉 **Вам доступна персональная промо-карточка!**\n"
            "Нажмите кнопку ниже, чтобы стереть защитное поле и узнать свой промокод."
        )
        button_text = "🎁 Стереть и получить подарок"
    else:
        app_url = WEBAPP_URL
        
        text = (
            f"👋 Привет, {message.from_user.first_name}!\n\n"
            "Добро пожаловать в сервис промо-игры. Запустите Mini App, чтобы участвовать в акциях!"
        )
        button_text = "🎰 Открыть игральную карту"

    # Прикрепляем прямую WebApp-кнопку
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=button_text, web_app=WebAppInfo(url=app_url))]
    ])

    await message.answer(text, reply_markup=keyboard, parse_mode="Markdown")

async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
