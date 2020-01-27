from asyncio import get_event_loop
from importlib import import_module
from pkgutil import walk_packages
from typing import List, Dict

from aiogram import Bot, Dispatcher
from telethon import TelegramClient

from config import CLIENTS, TOKEN

loop = get_event_loop()
bot = Bot(TOKEN, loop)
dp = Dispatcher(bot, loop)
commands: Dict[str, List[str]] = {}
clients: Dict[str, TelegramClient] = {k: TelegramClient(k, *v, loop=loop) for (k, v) in CLIENTS}


def load_package(package: str):
    package = import_module(package)
    for loader, name, is_pkg in walk_packages(package.__path__):
        full_name = f'{package.__name__}.{name}'
        plugin = import_module(full_name)
        if hasattr(plugin, 'commands'):
            commands[name] = plugin.commands

        if is_pkg:
            load_package(full_name)
