from asyncio import sleep

from telethon import TelegramClient
from telethon.events import register, NewMessage
from telethon.tl.custom import Message, Dialog

commands = ['.ra - read all dialogs']


@register(NewMessage(outgoing=True, pattern=r'=.ra'))
async def read_all(event: Message):
    count = 0
    client: TelegramClient = event.client
    dialog: Dialog
    async for dialog in client.iter_dialogs():
        if dialog.unread_count:
            await client.send_read_acknowledge(dialog.input_entity, max_id=dialog.message.id)
            count += 1

    await event.edit(f'Nailerine has marked {count} chats as read')
    await sleep(5)
    await event.delete()
