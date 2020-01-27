from telethon import TelegramClient
from telethon.events import NewMessage, register
from telethon.tl.custom import Message

commands = ['.u - no u']


@register(NewMessage(outgoing=True, pattern=r'\.u'))
async def no_u(event: Message):
    if event.is_reply:
        message: Message = await event.get_reply_message()
    else:
        client: TelegramClient = event.client
        async for m in client.iter_messages(await event.get_input_chat(), max_id=event.id):
            if not m.out:
                message: Message = m
                break
    user_id = message.from_id
    mention = f'no [u](tg://user?id={user_id})'

    if event.is_reply:
        await event.edit(mention)
    else:
        await event.delete()
        await message.reply(mention)
