import os
import aiohttp
import asyncio

from aiogram.filters import CommandStart
from aiogram import Bot, Dispatcher
from aiogram.types import Message
from dotenv import load_dotenv
from redis import RedisMiddleware

load_dotenv()

BOT_TOKEN = os.getenv('BOT_TOKEN')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
redis_middleware = RedisMiddleware()

API_URL = "http://127.0.0.1:8000/api/auth_telegram/"
@dp.message(CommandStart())
async def handle_start_command(message:Message):
    unique_token = message.get_agrs()
    user_id = message.from_user.id
    await redis_middleware.set_cache(user_id, unique_token)
    if not unique_token:
        await message.reply('Нет токена')
    await message.reply(
        "Привет! Введите ваши данные через запятую в формате: имя, фамилия, email\n"
        "Например: Иван, Иванов, ivan@example.com"
    )

@dp.message()
async def process_user_data(message: Message):
    data_user = message.text.strip()
    first_name, last_name, email = [i.strip() for i in data_user.split(",")]
    user_id = message.from_user.id
    unique_token = await redis_middleware.get_redis(user_id)
    json_in_Django = {
        'telegram_id': message.from_user.id,
        'telegram_username': first_name,
        'telegram_last_name': last_name,
        'telegram_email': email,
        'auth_token': unique_token
    }

    async with aiohttp.ClientSession()as session:
        async with session.post(API_URL, json=json_in_Django) as response:
            if response.status == 200:
                await message.reply('Регистрация прошла успешно')
            else:
                await message.replay(f'Ошибка {response.status}')


async def main():
    await redis_middleware.on_start()
    print("Redis подключен")
    await dp.start_polling(bot)
    await redis_middleware.on_stop()
    print("Redis отключен")

if __name__=='__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print('Exit')