import logging

from core.misc import loop, run


def setup_logging():
    fmt = '[%(levelname)s - %(asctime)s] %(name)s: %(message)s'
    logging.basicConfig(format=fmt, level=logging.INFO)


def main():
    setup_logging()
    loop.run_until_complete(run())


if __name__ == '__main__':
    main()