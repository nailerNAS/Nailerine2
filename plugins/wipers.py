import asyncio

from telethon import TelegramClient
from telethon.events import register, NewMessage
from telethon.tl.custom import Message
from telethon.tl.types import InputPeerSelf
from telethon.utils import get_display_name

from utils.wipers import Wipers

commands = ['.wom - wipe own messages',
            '.wam - wipe all messages']


@register(NewMessage(outgoing=True, pattern=r'\.wom'))
async def wipe_own_messages(event: Message):
    client: TelegramClient = event.client
    await event.delete()
    result = await Wipers.wipe(client, await event.get_input_chat(), own=True)
    chat = get_display_name(await event.get_chat())

    report = await client.send_message(InputPeerSelf(), f'Nailerine has deleted {result} messages from {chat}')

    await asyncio.sleep(10)
    await report.delete()


@register(NewMessage(outgoing=True, pattern=r'\.wam'))
async def wipe_all_messages(event: Message):
    client: TelegramClient = event.client
    result = await Wipers.wipe(client, await event.get_input_chat(), own=False)

    report = await event.respond(f'Nailerine has deleted {result} messages')

    await asyncio.sleep(10)
    await report.delete()
