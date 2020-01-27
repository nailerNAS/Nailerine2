from asyncio import get_event_loop
from importlib import import_module
from inspect import isawaitable
from pkgutil import walk_packages
from typing import List, Dict

from aiogram import Bot, Dispatcher
from telethon import TelegramClient

from config import CLIENTS, TOKEN

loop = get_event_loop()
bot = Bot(TOKEN, loop)
dp = Dispatcher(bot, loop)
plugins: Dict[str, List[str]] = {}
clients: Dict[str, TelegramClient] = {k: TelegramClient(k, *v, loop=loop) for (k, v) in CLIENTS}


def load_package(package: str):
    package = import_module(package)
    for loader, name, is_pkg in walk_packages(package.__path__):
        full_name = f'{package.__name__}.{name}'
        plugin = import_module(full_name)
        plugins[name] = plugin.commands if hasattr(plugin, 'commands') else None
        for item_name in dir(plugin):
            item = getattr(plugin, item_name)
            if isawaitable(item) and not item_name.startswith('_'):
                for client in clients.values():
                    client.add_event_handler(item)

        if is_pkg:
            load_package(full_name)


async def run():
    for client in clients.values():
        await client.start()
        await dp.skip_updates()
        try:
            await dp.start_polling(reset_webhook=True)
        except KeyboardInterrupt:
            await dp.stop_polling()
            for client in clients.values():
                await client.disconnect()
                await dp.wait_closed()
