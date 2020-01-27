from asyncio import get_event_loop, iscoroutinefunction
from importlib import import_module
from logging import getLogger
from pkgutil import walk_packages
from typing import List, Dict

from aiogram import Bot, Dispatcher
from telethon import TelegramClient

from config import CLIENTS, TOKEN

log = getLogger(__name__)

loop = get_event_loop()
bot = Bot(TOKEN, loop)
dp = Dispatcher(bot, loop)
plugins: Dict[str, List[str]] = {}
clients: Dict[str, TelegramClient] = {k: TelegramClient(f'./data/{k}.session', *v, loop=loop) for (k, v) in
                                      CLIENTS.items()}


def load_package(package: str):
    package = import_module(package)
    for loader, name, is_pkg in walk_packages(package.__path__):
        full_name = f'{package.__name__}.{name}'
        plugin = import_module(full_name)
        plugins[name] = plugin.commands if hasattr(plugin, 'commands') else None
        for item_name in dir(plugin):
            item = getattr(plugin, item_name)
            if iscoroutinefunction(item) and not item_name.startswith('_'):
                log.info('adding handler of %s to clients', name)
                for client in clients.values():
                    client.add_event_handler(item)
        log.info('loaded plugin %s', plugin)

        if is_pkg:
            load_package(full_name)


async def run():
    log.info('loading plugins')
    load_package('plugins')

    log.info('connecting clients')
    for client in clients.values():
        await client.start()

    log.info('starting polling')
    await dp.skip_updates()
    try:
        await dp.start_polling(reset_webhook=True)
    except KeyboardInterrupt:
        await dp.stop_polling()
        for client in clients.values():
            await client.disconnect()
            await dp.wait_closed()
