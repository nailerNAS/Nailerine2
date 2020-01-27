from telethon import TelegramClient
from telethon.hints import EntityLike


class Wipers:
    @staticmethod
    async def wipe(client: TelegramClient, entity: EntityLike, own: bool = True):
        message_ids = [m.id async for m in client.iter_messages(entity, from_user='me' if own else None)]
        await client.delete_messages(entity, message_ids)

        return len(message_ids)
