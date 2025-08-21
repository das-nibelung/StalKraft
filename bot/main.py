from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
import asyncio
import os
import logging

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI приложение
app = FastAPI()


# Модель для входящих данных
class Message(BaseModel):
    text: str
    chat_id: int


# Инициализация бота и диспетчера
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher()


# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Привет! Я бот, который пересылает сообщения с сайта в Telegram."
    )


# FastAPI эндпоинт для отправки сообщений
@app.post("/send_message")
async def send_message(message: Message):
    try:
        await bot.send_message(chat_id=message.chat_id, text=message.text)
        return {"status": "success"}
    except Exception as e:
        logger.error(f"Ошибка отправки сообщения: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# Функция для запуска polling
async def start_polling():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"Ошибка polling: {str(e)}")
        await asyncio.sleep(5)  # Задержка перед рестартом
        await start_polling()


# Запуск FastAPI и polling в одном процессе
async def main():
    # Регистрируем обработчики
    await dp.startup()

    # Запускаем polling в фоне
    asyncio.create_task(start_polling())


# Точка входа для Uvicorn
if __name__ == "__main__":
    import uvicorn

    # Запускаем FastAPI и polling
    asyncio.run(main())
    uvicorn.run(app, host="0.0.0.0", port=8001)
