from contextlib import redirect_stdout
from html import escape
from io import StringIO
from traceback import format_exc
from typing import Callable


class CodeRunners:
    @staticmethod
    def wrap_code(code: str) -> str:
        with StringIO() as string:
            string.write('async def __ex(event=None, client=None):\n')
            for line in code.splitlines(True):
                string.write(f'\t{line}')

            return string.getvalue()

    @classmethod
    def get_callable(cls, code: str) -> Callable:
        exec(cls.wrap_code(code))
        return locals()['__ex']

    @classmethod
    async def execute(cls, code: str, event=None, client=None):
        with StringIO() as stdout:
            with redirect_stdout(stdout):
                try:
                    fn = cls.get_callable(code)
                    await fn(event, client)
                except:
                    print(format_exc())

            return stdout.getvalue()

    @staticmethod
    def format_run(code: str, output: str, executor: str = 'Exec'):
        code = escape(code)
        output = escape(output)

        return f'<b>{executor}:</b>\n' \
               f'<code>{code}</code>\n\n' \
               f'<b>Output:</b>\n' \
               f'<code>{output}</code>'
