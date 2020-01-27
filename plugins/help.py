from logging import getLogger

from telethon.events import register, NewMessage
from telethon.tl.custom import Message

from core.misc import plugins

log = getLogger(__name__)

commands = ['.plugins - list plugins',
            '.help <plugin> - show plugin commands']


@register(NewMessage(outgoing=True, pattern=r'\.plugins'))
async def list_plugins(event: Message):
    log.info('sending plugin list to %s', event.chat_id)
    await event.edit('**Nailerine plugins:**\n\n' + '\n'.join(plugins.keys()))


@register(NewMessage(outgoing=True, pattern=r'\.help\s(?P<plugin>\w+)'))
async def list_plugin_commands(event: Message):
    plugin = event.pattern_match.group('plugin')
    log.info('sending command list for plugin %s to %s', plugin, event.chat_id)
    if plugin in plugins:
        if plugins[plugin]:
            await event.edit(f'Commands for **{plugin}**:\n\n' + '\n'.join(plugins[plugin]))
        else:
            await event.edit(f'**{plugin}** has no commands')
    else:
        await event.edit(f"Can't find plugin **{plugin}**")
