import io
from asyncio import gather

from telethon.events import register, NewMessage
from telethon.tl.custom import Message

from utils.code_runners import CodeRunners

commands = ['.ex <code> - execute python code, event and client objects will be passed']


@register(NewMessage(outgoing=True, pattern=r'(\.ex\s).+'))
async def run_exec(event: Message):
    cmd = event.pattern_match.group(1)
    code: str = event.raw_text
    code = code.replace(cmd, '', 1)

    output = await CodeRunners.execute(code, event, event.client)
    output = CodeRunners.format_run(code, output)

    if len(output) > 4096:
        output = output.replace('\n', '<br>')
        with io.BytesIO() as file:
            file.name = 'exec.html'
            file.write(output.encode())
            file.seek(0)

            await gather(event.delete(),
                         event.respond(file=file))
    else:
        await event.edit(output, parse_mode='html')
