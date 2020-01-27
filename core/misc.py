from asyncio import get_event_loop
from typing import List, Dict

from aiogram import Bot, Dispatcher
from telethon import TelegramClient

from config import CLIENTS, TOKEN

loop = get_event_loop()
bot = Bot(TOKEN, loop)
dp = Dispatcher(bot, loop)
commands: List[str] = []
clients: Dict[str, TelegramClient] = {k: TelegramClient(k, *v, loop=loop) for (k, v) in CLIENTS}
